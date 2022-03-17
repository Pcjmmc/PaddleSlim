// https://eslint.org/docs/user-guide/configuring

module.exports = {
  root: true,
  parser: 'babel-eslint',
  parserOptions: {
    sourceType: 'module'
  },
  env: {
    browser: true,
  },
  // https://github.com/standard/standard/blob/master/docs/RULES-en.md
  extends: 'standard',
  // required to lint *.vue files
  plugins: [
    'html',
    'vue'
  ],
  // add your custom rules here
  rules: {
    // allow paren-less arrow functions
    'arrow-parens': 0,
    'eqeqeq': 'off',
    'space-before-function-paren': 'off',
    'no-multi-spaces': 'off',
    'no-useless-escape': 0,
    'no-unused-vars': 'off',
    // allow async-await
    'generator-star-spacing': 0,
    // allow debugger during development
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'quotes': [0, 'single'], // 引号类型 `` "" ''
    'semi': 0, // [1, "always"]: 需要分号, [2, "never"]: 不加分号, 0: 禁用此项
    // [vue/no-parsing-error] Parsing error: x-invalid-end-tag
    'vue/html-self-closing': 'off',
    'vue/no-parsing-error': [2, {
      'x-invalid-end-tag': true,
    }],
    'indent': 'off',
    'camelcase': 'off'
  }
};
