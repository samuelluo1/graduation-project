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
          <v-btn text color="light-green" @click="$refs.menu.save(date); $router.push({name: 'item', query:{date: date}}); reload()">OK</v-btn>
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
        <v-icon>mdi-plus</v-icon>新增品項
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import Vue from 'vue'

export default {
  name: 'item',
  inject: ['reload'],
  data: () => ({
    isLoading: true,
    headers: [
      { title: '品項名稱',
        field: 'item_name',
        width: 500,
        titleAlign: 'center',
        columnAlign: 'center',
        isEdit: true,
        formatter: function (rowData, rowIndex, pagingIndex, field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`
        },
        isResize: true
      },
      { title: '品項價格', field: 'item_price', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '製作時間', field: 'time', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '售出量', field: 'sales', width: 100, titleAlign: 'center', columnAlign: 'center', isEdit: true, isResize: true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center', columnAlign: 'center', componentName: 'table-operation', isResize: true }
    ],
    dataList: [],
    monthData: [],
    isRouterAlive: true,
    date: new Date().toISOString().substr(0, 7),
    menu: false,
    id: this.$userId,
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
        .post('/post_item/', { item_name: '新品項', item_time: this.date})
        .then(itemRes => {
          this.$axios.get('/get_ingredient/').then(ingredientRes => {
            for (var i = 0; i < ingredientRes.data.length; i++) {
              this.$axios.post('/post_have/', { item: itemRes.data.id, ingredient: ingredientRes.data[i].id })
            }
          })
        })
      await this.reload()
    },
    cellEditDone (newValue, oldValue, rowIndex, rowData, field) {
      this.dataList[rowIndex][field] = newValue
      let params = {type: 'edit', index: this.index, rowData: this.rowData}
      if (field === 'item_name' && newValue.length > 30) {
        alert('名稱太長了!(超過三十字元)')
      } else if (field !== 'item_name' && parseFloat(newValue).toString() !== newValue) {
        alert('僅能輸入數字!')
      } else if (field !== 'item_name' && newValue < 0) {
        alert('不可輸入負號!')
      } else {
        this.$emit('on-custom-comp', params)
        this.$axios
          .put('/item/' + rowData.id + '/', {
            item_name: this.dataList[rowIndex]['item_name'],
            item_price: this.dataList[rowIndex]['item_price'],
            time: this.dataList[rowIndex]['time'],
            sales: this.dataList[rowIndex]['sales'],
            item_time: this.date,
            user: this.dataList[rowIndex]['user']
          })
      }
    },
    async addCopy (month) {
      this.btnIsDisabled = true
      await this.$axios.get('get_item').then(res => {
        var container = res.data.filter(a => a.item_time === month)
        for (var i = 0; i < container.length; i++) {
          container[i].item_time = this.date
          this.$axios.post('/post_item/', container[i])
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
    await this.$axios.get('/get_item/').then(res => {
      console.log(res.data)
      this.dataList = res.data.filter(a => a.item_time === this.date)
      for (var i = 0; i < res.data.length; i++) {
        if (!this.monthData.includes(res.data[i].item_time) && res.data[i].item_time !== this.date && this.monthData.length < 10) {
          this.monthData.push(res.data[i].item_time)
        }
      }
    })
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
      if (confirm('確定要刪除此品項?') && this.$emit('on-custom-comp', params)) {
        this.$axios.delete('/item/' + rowData.id + '/', { data: { username: 'root', password: 'ilovelibrary'} })
      }
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
