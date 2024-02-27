Vue.component('default', {
  template: `
<div>
  <h1>Sapling OpenThread network monitor</h1>
  <h2>Check Main Menu for options.</h2>
</div>`,
  mounted: function() {
    store.commit('title', 'Default')
  }
})

app.componentsLoaded('default')

