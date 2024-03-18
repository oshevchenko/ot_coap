Vue.component('product', {
  mixins: [crud, crud_front],
  data: function () {
    return {
      perpageAray: this.perpageAray,
      perpage: this.perpage
    }
  },
  template: `
<div>

  <div v-if="data">
    <product-table
      :rows="data"
      :perpage="perpage"
      @addRow="addRow()"
      @removeRow="removeRow($event)"
      @create="create_front($event)"
      @read="read_front($event)"
      @update="update_front($event)"
      @delete="delete_front($event)"
      />

    <div>On page: 
      | <span v-for="item in perpageAray">
          <a @click="setPerPage(item)" :class="perpage==item?'font-weight-bold':''">{{item}}</a> | 
        </span>
    </div>
    <div>
      <i>Parameter 'On page' stored in the application settings.</i>
    </div>

  </div>

</div>`,
  mounted: function() {
    store.commit('title', 'Product')
    this.instance = 'product'
    this.instance_url = location.origin.concat(appDataset[this.instance]['url'])
    this.read_front()
    this.perpageAray = [2, 3, 4, 6, 8, 12]
    this.perpage = app.getSettings('produсt.perpage', 4)
  },
  methods: {
    setPerPage: function (item) {
      this.perpage = item
      app.setSettings('produсt.perpage', this.perpage)
    },
    addRow: function () {
      this.data.push({'_edit_': true})
    },
    removeRow: function (row) {
      this.data.splice(this.data.indexOf(row), 1)
    }
  }
})

Vue.component('product-table', {
  mixins: [table],
  data: function () {
    return {
      filters: this.filters,
      currentFilter: this.currentFilter
    }
  },
  template: `
<div>

  <button @click="addRow()" class="btn btn-outline-primary float-right mb-1"><i class="fas fa-plus-square"></i> Create</button>

  <div class="m-3">
    Sort by (version #1): 
    | <span v-for="filter in filters"><a @click="currentFilter=filter" :class="currentFilter==filter?'font-weight-bold':''">{{filter.caption}}</a> | </span>
  </div>

  <div class="m-3">
    Sort by (version #2):
    <select v-model="currentFilter">
      <option></option>
      <option v-for="filter in filters" :value="filter">{{filter.caption}}</option>
    </select>
  </div>

  <div class="row">
    <div class="card float-left m-4" v-for="row in paginatedRows" style="width: 18rem;">
      <template v-if="row._edit_ == true">
        <div class="card-header">
          Code: <input type="text" v-model="row.code" size="15" required>
          <a @click="cancelEdit(row)" title="Cancel" class="float-right"><i class="fas fa-undo-alt"></i></a>
          <a @click="updateRow(row)" title="Save" class="float-right mr-2"><i class="fas fa-save text-success"></i></a>
        </div>
        <div class="card-body">
          <h5 class="card-title"><input type="text" v-model="row.name" style="width:100%" required></h5>
          <p class="card-text">$ <input type="number" step="0.01" v-model="row.price" required></p>
        </div>
      </template>
      <template v-else>
        <div class="card-header">
          Code: {{row.code}}
          <a @click="deleteRow(row)" title="Delete" class="float-right ml-2"><i class="fas fa-times text-danger"></i></a>
          <a @click="$set(row, '_edit_', true)" title="Edit" class="float-right"><i class="fas fa-edit"></i></a>
        </div>
        <div class="card-body">
          <h5 class="card-title">{{row.name}}</h5>
          <p class="card-text">$ {{row.price}}</p>
        </div>
      </template>

    </div>
  </div>

  <paginator v-bind:pages="pages" gap="5" v-bind:currentPage="currentPage" v-on:setPage="setPage($event)" v-on:setPrevPage="setPrevPage()" v-on:setNextPage="setNextPage()" class="text-center"></paginator>

</div>
  `,
mounted: function () {
  this.filters = [
    {'caption':'Name', 'field':'name', 'type':'string', 'reverse': false},
    {'caption':'Price', 'field':'price', 'type':'number', 'reverse': false},
    {'caption':'Price reverse', 'field':'price', 'type':'number', 'reverse': true}
  ]
  this.currentFilter = null
},
methods: {
  addRow: function () {
    this.currentPage = this.pages
    this.$emit('addRow')
  },
  updateRow: function (row) {
    row._edit_= null                // first disable edit mode
    this.$nextTick(()=> {           // then update view
      delete row._edit_             // after redrawing delete unnecessary field (_edit_)
      if (row.id) {
        this.$emit('update', row)   // finnaly update row
      }
      else {
        this.$emit('create', row)   // finnaly create row
      }
    })
  },
  deleteRow: function (row) {
    this.$emit('delete', row)
  },
  cancelEdit: function (row) {
    row._edit_= null
    this.$nextTick(()=> {
      delete row._edit_
      if (row.id) {
        this.$emit('read', row)
      }
      else {
        this.$emit('removeRow', row) // remove new record
      }
    })
  }
},
watch: {
  currentFilter() {
    if (this.currentFilter) {
      this.orderField = this.currentFilter.field
      this.orderFieldType = this.currentFilter.type
      this.orderReverse = this.currentFilter.reverse
    }
    else {
      this.orderField = ''
      this.orderFieldType = ''
      this.orderReverse = false
    }
  }
}
})

app.componentsLoaded('product')
