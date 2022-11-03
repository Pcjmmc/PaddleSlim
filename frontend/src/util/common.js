/**
 * Created by liuhuanling on 2020/11/11.
 */
// 菜单栏结构中英文对照
// export const menuDesc = {
//   // report: {
//   //   desc: '报告',
//   //   icon: 'ios-grid',
//   //   sub: {
//   //     single: {desc: '单个报告'},
//   //     frame: {desc: '框架天级'},
//   //     model: {desc: '模型天级'},
//   //     frelease: {desc: 'release回测'},
//   //     fbenchmark: {desc: 'api benchmark'},
//   //     package: {desc: '编包查询'}
//   //   },
//   //   notMenu: false
//   // },
//   quality: {
//     desc: '发版',
//     icon: 'ios-analytics',
//     sub: {
//       content: {
//         desc: '发版进度'
//       }
//     }
//   },
//   config: {
//     desc: 'case管理',
//     icon: 'ios-paper',
//     sub: {
//       sence_manager: {
//         desc: '场景管理'
//       },
//       tag_manager: {
//         desc: '标签管理'
//       }
//     }
//   },
//   detail: {
//     sub: {
//       function: {desc: '功能详情'},
//       model: {desc: '模型详情'},
//       'test-detail': {desc: '测试详情'},
//       'frame-api-detail': {desc: '基础框架详情'},
//       'commit-detail': {desc: 'commit 覆盖信息'}
//     },
//     notMenu: true
//   },
//   login: {
//     desc: '登录',
//     notMenu: true
//   }
// };

export const ColorList = ['#EDE234', '#F78436',
    '#E03DE0', '#366EF7', '#33F083',
    '#F20CBD', '#0D36FC', '#00E679',
    '#FFFE00', '#F57E0F', '#F0BF00',
    '#F73700', '#9F00E0', '#007EF7',
    '#00F038', '#F0A700', '#F71400',
    '#6500E0', '#00BEF7', '#0DF000',
    '#F06E00', '#F700AF', '#0113E0',
    '#00F7AB', '#B2F000'
];

export const TestServerMap = {
    op_function: '计算OP精度测试',
    external_api_function: '功能性API测试',
    distribution_api_function: '分布式API功能测试',
    jit_function: 'JIT API单独组网测试',
    native_infer: '原生推理',
    trt_infer: 'TensorRT推理',
    mkldnn_infer: 'MKLDNN推理',
    models_benchmark_v100_single_dp: 'V100_单机性能测试',
    models_benchmark_v100_multi_dp: 'V100_多机性能测试',
    models_benchmark_v100_dist_collective: 'V100_分布式性能测试',
    distribution_v100_accuracy_collective: 'V100_分布式精度测试',
    models_benchmark_a100_single_dp: 'A100_单机性能测试',
    models_benchmark_a100_multi_dp: 'A100_多机性能测试'
};
