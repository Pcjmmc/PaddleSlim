import Vue from 'vue'
import Modal from './Modal.vue'

const prefixCls = 'ivu-modal-confirm'

Modal.newInstance = properties => {
  const _props = properties || {}

  const Instance = new Vue({
    data: Object.assign({}, _props, {
      visible: false,
      width: 416,
      title: '',
      body: '',
      iconType: '',
      iconName: '',
      okText: undefined,
      cancelText: undefined,
      showCancel: false,
      loading: false,
      buttonLoading: false,
      scrollable: false
    }),
    render (h) {
      let footerVNodes = []
      if (this.showCancel) {
        footerVNodes.push(h('Button', {
          props: {
            type: 'text',
            size: 'large'
          },
          on: {
            click: this.cancel
          }
        }, this.localeCancelText))
      }
      footerVNodes.push(h('Button', {
        props: {
          type: 'primary',
          size: 'large',
          loading: this.buttonLoading
        },
        on: {
          click: this.ok
        }
      }, this.localeOkText))

      // render content
      let bodyRender
      if (this.render) {
        bodyRender = h('div', {
          attrs: {
            class: `${prefixCls}-body ${prefixCls}-body-render`
          }
        }, [this.render(h)])
      } else {
        bodyRender = h('div', {
          attrs: {
            class: `${prefixCls}-body`
          }
        }, [
          h('div', {
            class: this.iconTypeCls
          }, [
            h('i', {
              class: this.iconNameCls
            })
          ]),
          h('div', {
            domProps: {
              innerHTML: this.body
            }
          })
        ])
      }

      return h(Modal, {
        props: Object.assign({}, _props, {
          width: this.width,
          scrollable: this.scrollable
        }),
        domProps: {
          value: this.visible
        },
        on: {
          input: (status) => {
            this.visible = status
          }
        }
      }, [
        h('div', {
          attrs: {
            class: prefixCls
          }
        }, [
          h('div', {
            attrs: {
              class: `${prefixCls}-head`
            }
          }, [
            h('div', {
              attrs: {
                class: `${prefixCls}-head-title`
              },
              domProps: {
                innerHTML: this.title
              }
            })
          ]),
          bodyRender,
          h('div', {
            attrs: {
              class: `${prefixCls}-footer`
            }
          }, footerVNodes)
        ])
      ])
    },
    computed: {
      iconTypeCls () {
        return [
          `${prefixCls}-body-icon`,
          `${prefixCls}-body-icon-${this.iconType}`
        ]
      },
      iconNameCls () {
        return [
          'ivu-icon',
          `ivu-icon-${this.iconName}`
        ]
      },
      localeOkText () {
        if (this.okText) {
          return this.okText
        } else {
          return '确定(Q)'
        }
      },
      localeCancelText () {
        if (this.cancelText) {
          return this.cancelText
        } else {
          return '取消'
        }
      }
    },
    mounted () {
      document.addEventListener('keydown', this.EscClose)
      document.addEventListener('keydown', this.SpaceOk)
    },
    beforeDestroy () {
      document.removeEventListener('keydown', this.EscClose)
      document.removeEventListener('keydown', this.SpaceOk)
    },
    methods: {
      cancel () {
        console.log('cancel this.$children[0]', this.$children[0])
        this.$children[0].visible = false
        this.buttonLoading = false
        this.onCancel()
        this.remove()
      },
      ok () {
        if (this.loading) {
          this.buttonLoading = true
        } else {
          this.$children[0].visible = false
          this.remove()
        }
        this.onOk()
      },
      remove () {
        setTimeout(() => {
          this.destroy()
        }, 300)
      },
      destroy () {
        this.$destroy()
        document.body.removeChild(this.$el)
        this.onRemove()
      },
      onOk () {},
      onCancel () {},
      onRemove () {},
      EscClose (e) {
        if (this.$children[0].visible) {
          if (e.keyCode === 27) {
            this.cancel()
          }
        }
      },
      SpaceOk (e) {
        if (this.$children[0].visible) {
          if (e.keyCode === 81) {
            this.ok()
          }
        }
      }
    }
  })

  const component = Instance.$mount()
  document.body.appendChild(component.$el)
  const modal = Instance.$children[0]

  return {
    show (props) {
      modal.$parent.showCancel = props.showCancel
      modal.$parent.iconType = props.icon

      switch (props.icon) {
        case 'info':
          modal.$parent.iconName = 'information-circled'
          break
        case 'success':
          modal.$parent.iconName = 'checkmark-circled'
          break
        case 'warning':
          modal.$parent.iconName = 'android-alert'
          break
        case 'error':
          modal.$parent.iconName = 'close-circled'
          break
        case 'confirm':
          modal.$parent.iconName = 'help-circled'
          break
      }

      if ('width' in props) {
        modal.$parent.width = props.width
      }

      if ('closable' in props) {
        modal.$parent.closable = props.closable
      }

      if ('title' in props) {
        modal.$parent.title = props.title
      }

      if ('content' in props) {
        modal.$parent.body = props.content
      }

      if ('okText' in props) {
        modal.$parent.okText = props.okText
      }

      if ('cancelText' in props) {
        modal.$parent.cancelText = props.cancelText
      }

      if ('onCancel' in props) {
        modal.$parent.onCancel = props.onCancel
      }

      if ('onOk' in props) {
        modal.$parent.onOk = props.onOk
      }

      // async for ok
      if ('loading' in props) {
        modal.$parent.loading = props.loading
      }

      if ('scrollable' in props) {
        modal.$parent.scrollable = props.scrollable
      }

      // notice when component destroy
      modal.$parent.onRemove = props.onRemove

      modal.visible = true
    },
    remove () {
      modal.visible = false
      modal.$parent.buttonLoading = false
      modal.$parent.remove()
    },
    component: modal
  }
}

export default Modal
