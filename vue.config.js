module.exports = {
    "lintOnSave": false,

    "pluginOptions": {
        "electronBuilder": {
            "nodeIntegration": true
        }
    },

    "transpileDependencies": [
        "vuetify"
    ],

    pluginOptions: {
      electronBuilder: {
        nodeIntegration: true
      },
      i18n: {
        locale: 'en',
        fallbackLocale: 'fr',
        localeDir: 'locales',
        enableInSFC: true
      }
    }
}
