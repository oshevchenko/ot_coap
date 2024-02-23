Vue.component('default', {
  template: `
<div>
  <h1>Frontend + Backend</h1>
  <h2>Работа с базой данных</h2>
</div>`,
  mounted: function() {
    store.commit('title', 'Default')
  }
})

app.componentsLoaded('default')
