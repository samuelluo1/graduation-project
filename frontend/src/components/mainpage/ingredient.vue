<template>
  <div>
    <v-card>
      <v-table
        is-horizontal-resize
        :is-loading="isLoading"
        style="width:100%"
        :columns="headers"
        :table-data="dataList"
        row-hover-color="#F1F8E9"
        row-click-color="#F1F8E9"
        :cell-edit-done="cellEditDone"
        @on-custom-comp="customCompFunc"
      ></v-table>
      <v-btn small color='white' @click='add'>
        <v-icon>mdi-plus</v-icon>新增原料
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'ingredient',
  inject: ['reload'],
  data: () => ({
    headers: [
      { title: '原料名稱',
        field: 'ingredient_name',
        width: 500,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '原料花費', field: 'ingredient_price', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true }
    ],
    dataList: [],
    itemIdList: [],
    itemLength: '',
    isRouterAlive: true
  }),
  methods: {
    customCompFunc (params) {
      if (params.type === 'delete') {
        this.$delete(this.dataList, params.index)
      }
    },
    add () {
      this.$axios
        .post('/ingredient/', { ingredient_name: '新原料' })
        .then(res => {
          for (var i = 0; i < this.itemIdList.length; i++) {
            this.$axios.post('/have/', { item: this.itemIdList[i], ingredient: res.data.id })
          }
          this.reload()
        })
    },
    cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = { type: 'edit', index: this.index, rowData: this.rowData }
      if (field === 'ingredient_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'ingredient_name' && parseFloat(newValue).toString() !== newValue) {
        alert('僅能輸入數字!')
      } else if (field !== 'ingredient_name' && newValue < 0) {
        alert('不可輸入負號!')
      } else if (field === 'ingredient_name' | field === 'ingredient_price') {
        this.dataList[rowIndex][field] = newValue
        this.$axios
          .put('/ingredient/' + rowData.id + '/', {
            ingredient_name: this.dataList[rowIndex]['ingredient_name'],
            ingredient_price: this.dataList[rowIndex]['ingredient_price']
          })
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios.get('/have/?ingredient=' + rowData.id + '&item=' + field.substr(5))
          .then(res => {
            this.$axios.put('/have/' + res.data[0].id + '/', { proportion: newValue })
          })
      }
    }
  },
  created () {
    this.isLoading = true
    this.$axios.all([this.$axios.get('/ingredient/'), this.$axios.get('/item/'), this.$axios.get('/have/')])
      .then(this.$axios.spread((ingrResp, itemResp, haveResp) => {
        this.dataList = ingrResp.data
        this.itemLength = itemResp.data.length
        for (var i = 0; i < this.itemLength; i++) {
          var itemId = itemResp.data[i].id
          var name = itemResp.data[i].item_name
          this.headers.push({ title: name + '所占比例', field: 'item_' + itemId, width: 120, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true })
          this.itemIdList.push(itemId)
          for (var j = 0; j < this.dataList.length; j++) {
            this.$set(this.dataList[j], 'item_' + itemId, haveResp.data.filter(a => a.item === itemId).filter(b => b.ingredient === ingrResp.data[j].id)[0].proportion)
          }
        }
        this.headers.push({ title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true })
        this.isLoading = false
      }))
  }
}
Vue.component('table-operation', {
  template: `<span><a href="" @click.stop.prevent="deleteRow(rowData,index)" style="color:red">刪除</a></span>`,
  props: {
    rowData: { type: Object },
    field: { type: String },
    index: { type: Number }
  },
  methods: {
    deleteRow (rowData, index) {
      let params = {type: 'delete', index: this.index}
      confirm('確定要刪除此品項?') && this.$emit('on-custom-comp', params)
      this.$axios.delete('/ingredient/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary' } })
    }
  }
})
</script>

<style scoped>
    .cell-edit-color{
        color: #8BC34A;
        font-weight: bold;
    }
</style>
