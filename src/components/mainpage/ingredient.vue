<template>
  <div>
    <v-row align="baseline" justify="space-around">
    <v-col md="2">
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        :return-value.sync="date"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            color='light-green'
            v-model="date"
            placeholder=" 請選擇年月份"
            readonly
            prepend-icon="event"
            v-bind="attrs"
            v-on="on"
            hide-details
            class="ma-0 pa-0"
          ></v-text-field>
        </template>
        <v-date-picker
          color='light-green'
          v-model="date"
          type="month"
          no-title
          scrollable
        >
          <v-btn text color="light-green" @click="menu = false">Cancel</v-btn>
          <v-btn text color="light-green" @click="$refs.menu.save(date); $router.push({name: 'ingredient', query:{date: date}}); reload()">OK</v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
    <v-col md="2" >
    <v-menu
        offset-y
      >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="light-green"
          dark
          v-bind="attrs"
          v-on="on"
          :disabled=btnIsDisabled
        >
          複製
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in monthData"
          :key="index"
          @click="addCopy(item)"
        >
          <v-list-item-title>{{ item }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    </v-col>
    </v-row>
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
      <v-btn small color='white' @click='add' :disabled=btnIsDisabled>
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
    monthData: [],
    itemLength: '',
    isRouterAlive: true,
    date: new Date().toISOString().substr(0, 7),
    menu: false,
    btnIsDisabled: true
  }),
  methods: {
    customCompFunc (params) {
      if (params.type === 'delete') {
        this.$delete(this.dataList, params.index)
      }
    },
    async add () {
      this.btnIsDisabled = true
      await this.$axios
        .post('/post_ingredient/', { ingredient_name: '新原料', ingredient_time: this.date })
        .then(res => {
          for (var i = 0; i < this.itemIdList.length; i++) {
            this.$axios.post('/post_have/', { item: this.itemIdList[i], ingredient: res.data.id, proportion: '0' })
          }
        })
      await this.reload()
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
            id: rowData.id,
            ingredient_name: this.dataList[rowIndex]['ingredient_name'],
            ingredient_price: this.dataList[rowIndex]['ingredient_price'],
            ingredient_time: this.date,
            user: this.dataList[rowIndex]['user']
          })
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios.get('/get_have/?ingredient=' + rowData.id + '&item=' + field.substr(5))
          .then(res => {
            var haveId = res.data.filter(b => b.item == field.substr(5)).filter(a => a.ingredient === rowData.id)[0].id
            this.$axios.put('/have/' + haveId + '/', { id: haveId, proportion: newValue, ingredient: rowData.id, item: field.substr(5), user: this.dataList[rowIndex]['user'] })
          })
      }
    },
    async addCopy (month) {
      this.btnIsDisabled = true
      await this.$axios.get('/get_ingredient/').then(res_a => {
        var container = res_a.datafilter(a => a.ingredient_time === month)
        var $this = this
        function postHave (i, j) {
          $this.$axios.post('/post_have/', { item: $this.itemIdList[i], ingredient: j.data.id, proportion: '0' })
        }
        for (var i = 0; i < container.length; i++) {
          container[i].ingredient_time = this.date
          this.$axios
            .post('/post_ingredient/', container[i])
            .then(res_b => {
              for (var j = 0; j < this.itemIdList.length; j++) {
                postHave(j, res_b)
              }
            })
        }
      })
      await this.reload()
    }
  },
  async created () {
    this.isLoading = true
    if (this.$route.query.date !== undefined) {
      this.date = this.$route.query.date
    }
    await this.$axios.all([this.$axios.get('/get_ingredient/'), this.$axios.get('/get_item/'), this.$axios.get('/get_have/')])
      .then(this.$axios.spread((ingrResp, itemResp, haveResp) => {
        this.dataList = ingrResp.data.filter(a => a.ingredient_time === this.date)
        var itemData = itemResp.data.filter(a => a.item_time === this.date)
        this.itemLength = itemData.length
        for (var i = 0; i < this.itemLength; i++) {
          var itemId = itemData[i].id
          var name = itemData[i].item_name
          this.headers.push({ title: name + '所占比例', field: 'item_' + itemId, width: 120, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true })
          this.itemIdList.push(itemId)
          for (var j = 0; j < this.dataList.length; j++) {
            console.log(itemId, this.dataList[j].id)
            this.$set(this.dataList[j], 'item_' + itemId, haveResp.data.filter(a => a.item === itemId).filter(b => b.ingredient === this.dataList[j].id)[0].proportion)
          }
        }
        this.headers.push({ title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: false, componentName: 'table-operation', isResize: true })
        for (var k = 0; k < ingrResp.data.length; k++) {
          if (!this.monthData.includes(ingrResp.data[k].ingredient_time) && ingrResp.data[k].ingredient_time !== this.date && this.monthData.length < 10) {
            this.monthData.push(ingrResp.data[k].ingredient_time)
          }
        }
      }))
    this.btnIsDisabled = false
    this.isLoading = false
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
