const { defineConfig } = require('cypress')

module.exports = defineConfig({
  env: {
    apiUrl: 'http://localhost:8000',
    supportFile: false,
  },
  e2e: {
    setupNodeEvents(on, config) {},
  },
})
