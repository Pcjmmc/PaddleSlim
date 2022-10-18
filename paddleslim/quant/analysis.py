# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import pickle
import copy
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import random
import tempfile
import paddle
from paddle.fluid import core
from paddle.fluid import framework
from paddle.fluid.framework import IrGraph
from paddle.fluid.executor import global_scope
from paddle.fluid.contrib.slim.quantization import PostTrainingQuantization
from paddle.fluid.contrib.slim.quantization.utils import _get_op_input_var_names, load_variable_data
from .quanter import quant_post
from ..core import GraphWrapper
from ..common import get_logger
from ..common import get_feed_vars, wrap_dataloader, load_inference_model, get_model_dir

_logger = get_logger(__name__, level=logging.INFO)

__all__ = ["AnalysisQuant"]


class AnalysisQuant(object):
    def __init__(self,
                 model_dir,
                 model_filename=None,
                 params_filename=None,
                 eval_function=None,
                 data_loader=None,
                 save_dir='analysis_results',
                 num_histogram_plots=10,
                 resume=False,
                 ptq_config=None):
        """
        AnalysisQuant provides to analysis the sensitivity of each op in the model.
        
        Args:
            model_dir(str): the path of fp32 model that will be quantized, it can also be '.onnx'
            model_filename(str, optional): the model file name of the fp32 model
            params_filename(str, optional): the parameter file name of the fp32 model
            eval_function(function): eval function, define by yourself to return the metric of the inference program, can be used to judge the metric of quantized model.  (TODO: optional)
            data_loader(Python Generator, Paddle.io.DataLoader, optional): the
                Generator or Dataloader provides calibrate data, and it could
                return a batch every time
            save_dir(str, optional): the output dir that stores the analyzed information
            resume(bool, optional): When break off while ananlyzing, could resume analysis program and load already analyzed information.
            ptq_config(dict, optional): the args that can initialize PostTrainingQuantization
            
        """
        if model_filename is None:
            model_filename = 'model.pdmodel'
        if params_filename is None:
            params_filename = 'model.pdiparams'
        self.model_dir = model_dir
        self.model_filename = model_filename
        self.params_filename = params_filename
        self.histogram_bins = 1000
        self.save_dir = save_dir
        self.eval_function = eval_function
        self.quant_layer_names = []
        self.checkpoint_name = os.path.join(save_dir, 'analysis_checkpoint.pkl')
        self.quant_layer_metrics = {}
        self.num_histogram_plots = num_histogram_plots
        self.ptq_config = ptq_config
        self.batch_nums = ptq_config[
            'batch_nums'] if 'batch_nums' in ptq_config else 10
        self.is_full_quantize = ptq_config[
            'is_full_quantize'] if 'is_full_quantize' in ptq_config else False
        self.onnx_format = ptq_config[
            'onnx_format'] if 'onnx_format' in ptq_config else False

        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        if self.onnx_format:
            self.temp_root_path = tempfile.TemporaryDirectory(dir=self.save_dir)
            self.temp_save_path = os.path.join(self.temp_root_path.name, "ptq")
            if not os.path.exists(self.temp_save_path):
                os.makedirs(self.temp_save_path)

        devices = paddle.device.get_device().split(':')[0]
        self.places = paddle.device._convert_to_place(devices)
        executor = paddle.static.Executor(self.places)

        # load model 
        [program, self.feed_list, self.fetch_list]= load_inference_model( \
            self.model_dir, \
            executor=executor, \
            model_filename=self.model_filename, \
            params_filename=self.params_filename)

        # create data_loader
        self.data_loader = wrap_dataloader(data_loader, self.feed_list)

        # evaluate before quant 
        # TODO: self.eval_function can be None
        if self.eval_function is not None:
            self.base_metric = self.eval_function(
                executor, program, self.feed_list, self.fetch_list)
            _logger.info('Before quantized, the accuracy of the model is: {}'.
                         format(self.base_metric))

        # quant and evaluate after quant (skip_list = None)
        post_training_quantization = PostTrainingQuantization(
            executor=executor,
            data_loader=self.data_loader,
            model_dir=self.model_dir,
            model_filename=self.model_filename,
            params_filename=self.params_filename,
            skip_tensor_list=None,
            algo='avg',  #fastest
            onnx_format=self.onnx_format,
            **self.ptq_config)
        program = post_training_quantization.quantize()
        if self.onnx_format:
            post_training_quantization.save_quantized_model(
                self.temp_save_path,
                model_filename='model.pdmodel',
                params_filename='model.pdiparams')
            program, _, _ = load_inference_model(
                self.temp_save_path,
                executor,
                model_filename='model.pdmodel',
                params_filename='model.pdiparams')
        self.quant_metric = self.eval_function(executor, program,
                                               self.feed_list, self.fetch_list)
        _logger.info('After quantized, the accuracy of the model is: {}'.format(
            self.quant_metric))

        # get quantized weight and act var name
        self.quantized_weight_var_name = post_training_quantization._quantized_weight_var_name
        self.quantized_act_var_name = post_training_quantization._quantized_act_var_name
        self.support_quant_val_name_list = self.quantized_weight_var_name if not self.is_full_quantize else list(
            self.quantized_act_var_name)
        executor.close()

        # load tobe_analyized_layer from checkpoint
        if resume:
            self.load_checkpoint()
        self.tobe_analyized_layer = set(self.support_quant_val_name_list) - set(
            list(self.quant_layer_metrics.keys()))
        self.tobe_analyized_layer = sorted(list(self.tobe_analyized_layer))

    def compute_quant_sensitivity(self, plot_hist=True):
        '''
        compute the sensitivity of quantized layers by eval function
        '''
        assert self.data_loader is not None, "When computing the sensitivity of quantized layers, the data loader is needed"
        assert self.eval_function is not None, "When computing the sensitivity of quantized layers, the eval function is needed"
        self.eval_quant_model()
        self.sensitivity_ranklist = sorted(
            self.quant_layer_metrics,
            key=self.quant_layer_metrics.get,
            reverse=False)

        _logger.info('Finished computing the sensitivity of the model.')
        for name in self.sensitivity_ranklist:
            _logger.info("quant layer name: {}, eval metric: {}".format(
                name, self.quant_layer_metrics[name]))

        analysis_file = os.path.join(self.save_dir, "analysis.txt")
        with open(analysis_file, "w") as analysis_ret_f:
            for name in self.sensitivity_ranklist:
                analysis_ret_f.write(
                    "quant layer name: {}, eval metric: {}\n".format(
                        name, self.quant_layer_metrics[name]))
        _logger.info('Analysis file is saved in {}'.format(analysis_file))

        if plot_hist:
            self.calculate_histogram()

    def save_checkpoint(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        with open(self.checkpoint_name, 'wb') as f:
            pickle.dump(self.quant_layer_metrics, f)
        _logger.info('save checkpoint to {}'.format(self.checkpoint_name))

    def load_checkpoint(self):
        if not os.path.exists(self.checkpoint_name):
            return False
        with open(self.checkpoint_name, 'rb') as f:
            self.quant_layer_metrics = pickle.load(f)
        _logger.info('load checkpoint from {}'.format(self.checkpoint_name))
        return True

    def plot_activation_distribution(self, axis=None):
        '''
        Collect and plot the distribution of the activation of each weight layer.
        '''
        devices = paddle.device.get_device().split(':')[0]
        places = paddle.device._convert_to_place(devices)
        executor = paddle.static.Executor(places)

        [program, feed_list, fetch_list]= load_inference_model( \
            self.model_dir, \
            executor=executor, \
            model_filename=self.model_filename, \
            params_filename=self.params_filename)

        scope = global_scope()

        persistable_var_names = []
        for var in program.list_vars():
            if var.persistable:
                persistable_var_names.append(var.name)

        weight_names = sorted(list(self.quantized_weight_var_name))
        acts_weight_map = self.get_weight_act_map(program, weight_names,
                                                  persistable_var_names)
        all_acts = list(acts_weight_map.keys())
        all_weights = [acts_weight_map[act] for act in all_acts]
        act_distribution = []
        for var_name in all_acts:
            var_tensor = load_variable_data(scope, var_name)
            if axis is None:
                var_tensor = var_tensor.flatten()
            else:
                var_tensor = var_tensor.reshape(
                    [-1, var_tensor.shape[axis]]).abs().max(axis=-1)
            sample_num = len(var_tensor) if len(var_tensor) < 1000 else 1000
            var_tensor = random.sample(list(var_tensor), sample_num)
            act_distribution.append(var_tensor)

        all_values = sum(act_distribution, [])
        max_value = np.max(all_values)
        min_value = np.min(all_values)
        pdf_path = os.path.join(self.save_dir, 'activation_distribution.pdf')
        with PdfPages(pdf_path) as pdf:
            for i in range(0, len(act_distribution), 20):
                r = i + 20 if i + 20 < len(act_distribution) else len(
                    act_distribution)
                plt.boxplot(
                    act_distribution[i:r],
                    labels=all_weights[i:r],
                    showbox=True,
                    patch_artist=True)
                plt.xticks(rotation=90)
                plt.tick_params(axis='x')
                plt.ylim([min_value, max_value])
                plt.xlabel('Weight Name')
                plt.ylabel("Activation Distribution")
                plt.tight_layout()
                plt.show()
                pdf.savefig()
                plt.close()
        _logger.info('Distribution plots is saved in {}'.format(pdf_path))

    def eval_quant_model(self):
        '''
        For each layer, quantize the weight op and evaluate the quantized model.
        '''
        for i, layer_name in enumerate(self.tobe_analyized_layer):
            _logger.info('Checking {}/{} quant model: quant layer {}'.format(
                i + 1, len(self.tobe_analyized_layer), layer_name))
            skip_list = copy.copy(list(self.support_quant_val_name_list))
            skip_list.remove(layer_name)

            executor = paddle.static.Executor(self.places)
            post_training_quantization = PostTrainingQuantization(
                executor=executor,
                data_loader=self.data_loader,
                model_dir=self.model_dir,
                model_filename=self.model_filename,
                params_filename=self.params_filename,
                skip_tensor_list=skip_list,
                onnx_format=self.onnx_format,
                algo='avg',  #fastest
                **self.ptq_config)
            program = post_training_quantization.quantize()
            _logger.info('Evaluating...')
            if self.onnx_format:
                post_training_quantization.save_quantized_model(
                    self.temp_save_path,
                    model_filename='model.pdmodel',
                    params_filename='model.pdiparams')
                program, _, _ = load_inference_model(
                    self.temp_save_path,
                    executor,
                    model_filename='model.pdmodel',
                    params_filename='model.pdiparams')
            quant_metric = self.eval_function(executor, program, self.feed_list,
                                              self.fetch_list)
            executor.close()
            _logger.info(
                "Quantized layer name: {}, eval metric: {}, the loss caused by this layer: {}".
                format(layer_name,
                       round(quant_metric, 4),
                       round(self.base_metric - quant_metric, 4)))
            self.quant_layer_metrics[layer_name] = quant_metric
            self.save_checkpoint()
        if self.onnx_format:
            self.temp_root_path.cleanup()

    def get_weight_act_map(self, program, weight_names, persistable_var_names):
        act_names = {}
        for op_name in weight_names:
            for block_id in range(len(program.blocks)):
                for op in program.blocks[block_id].ops:
                    var_name_list = _get_op_input_var_names(op)
                    if op_name in var_name_list:
                        for var_name in var_name_list:
                            if var_name not in persistable_var_names:
                                act_names[var_name] = op_name
        return act_names

    def get_hist_ops_name(self, graph, program):
        if self.num_histogram_plots <= 0:
            return []

        best_weight_ops = self.sensitivity_ranklist[::-1][:self.
                                                          num_histogram_plots]
        worst_weight_ops = self.sensitivity_ranklist[:self.num_histogram_plots]

        persistable_var_names = []
        for var in program.list_vars():
            if var.persistable:
                persistable_var_names.append(var.name)

        best_acts = self.get_weight_act_map(program, best_weight_ops,
                                            persistable_var_names)
        worst_acts = self.get_weight_act_map(program, worst_weight_ops,
                                             persistable_var_names)
        return [best_weight_ops, best_acts, worst_weight_ops, worst_acts]

    def collect_tensors_histogram(self, scope, ops):
        hist = {}
        for var_name in ops:
            var_tensor = load_variable_data(scope, var_name)
            var_tensor = np.array(var_tensor)
            min_v = float(np.min(var_tensor))
            max_v = float(np.max(var_tensor))
            var_tensor = var_tensor.flatten()
            _, hist_edges = np.histogram(
                var_tensor.copy(),
                bins=self.histogram_bins,
                range=(min_v, max_v))
            hist[var_name] = [var_tensor, hist_edges]
        return hist

    def calculate_histogram(self):
        '''
        Sample histograms for the weight and corresponding act tensors
        '''
        devices = paddle.device.get_device().split(':')[0]
        places = paddle.device._convert_to_place(devices)
        executor = paddle.static.Executor(places)

        [program, feed_list, fetch_list]= load_inference_model( \
            self.model_dir, \
            executor=executor, \
            model_filename=self.model_filename, \
            params_filename=self.params_filename)

        scope = global_scope()

        graph = IrGraph(core.Graph(program.desc), for_test=False)
        tensors_tobe_draw_hist = self.get_hist_ops_name(graph, program)
        if not tensors_tobe_draw_hist:
            return

        for var in program.list_vars():
            if var.name in self.quantized_act_var_name:
                var.persistable = True

        # sample before collect histogram
        batch_id = 0
        for data in self.data_loader():
            executor.run(program=program,
                         feed=data,
                         fetch_list=fetch_list,
                         return_numpy=False,
                         scope=scope)
            batch_id += 1
            if batch_id >= self.batch_nums:
                break

        pdf_names = [
            'best_weight_hist_result.pdf',
            'best_act_hist_result.pdf',
            'worst_weight_hist_result.pdf',
            'worst_act_hist_result.pdf',
        ]
        for tensors, save_pdf_name in zip(tensors_tobe_draw_hist, pdf_names):
            if isinstance(tensors, list):
                hist_data = self.collect_tensors_histogram(scope, tensors)
                self.draw_hist_pdf(hist_data, save_pdf_name, None)
            else:
                hist_data = self.collect_tensors_histogram(scope,
                                                           list(tensors.keys()))
                self.draw_hist_pdf(hist_data, save_pdf_name, tensors)

    def draw_hist_pdf(self, hist_data, save_pdf_name, weight_act_map):
        pdf_path = os.path.join(self.save_dir, save_pdf_name)
        with PdfPages(pdf_path) as pdf:
            for name in hist_data:
                plt.hist(hist_data[name][0], bins=hist_data[name][1])
                plt.xlabel(name)
                plt.ylabel("Frequency")
                if 'act' in save_pdf_name:
                    plt.title("Hist of Activation {}/Input of Weight {}".format(
                        name, weight_act_map[name]))
                else:
                    plt.title("Hist of Weight {}".format(name))
                plt.show()
                pdf.savefig()
                plt.close()
        _logger.info('Histogram plot is saved in {}'.format(pdf_path))

    def get_target_quant_model(self, target_metric):
        _logger.info(
            'Start to Find quant model that satisfies the target metric.')
        _logger.info(
            'Make sure that you are using full eval dataset to get target quantized model.'
        )
        skip_list = []
        rank_list = copy.copy(self.sensitivity_ranklist)
        while True:
            skip_list.append(rank_list.pop(0))
            _logger.info('Skip Ops: {}'.format(skip_list))
            executor = paddle.static.Executor(self.places)
            post_training_quantization = PostTrainingQuantization(
                executor=executor,
                data_loader=self.data_loader,
                model_dir=self.model_dir,
                model_filename=self.model_filename,
                params_filename=self.params_filename,
                onnx_format=self.onnx_format,
                skip_tensor_list=skip_list,
                **self.ptq_config)
            program = post_training_quantization.quantize()

            _logger.info('Evaluating...')
            quant_metric = self.eval_function(executor, program, self.feed_list,
                                              self.fetch_list)
            _logger.info("Current eval metric: {}, the target metric: {}".
                         format(quant_metric, target_metric))
            if quant_metric >= target_metric:
                quantize_model_path = os.path.join(self.save_dir,
                                                   'target_quant_model')
                _logger.info(
                    'The quantized model satisfies the target metric and is saved to {}'.
                    format(quantize_model_path))
                post_training_quantization.save_quantized_model(
                    quantize_model_path,
                    model_filename='model.pdmodel',
                    params_filename='model.pdiparams')
                break
            else:
                _logger.info(
                    'The quantized model does not satisfy the target metric. Skip next Op...'
                )
            executor.close()