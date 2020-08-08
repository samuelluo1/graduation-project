<template>
  <div>  
    <v-card>     
        <v-table
            is-horizontal-resize
            style="width:100%"
            :columns="headers"
            :table-data="dataList"
            row-hover-color="#F1F8E9"
            row-click-color="#F1F8E9"
            :cell-edit-done="cellEditDone"
            @on-custom-comp="customCompFunc"
        ></v-table>
    
            <v-btn small color='white' @click='add'>
              <v-icon>mdi-plus</v-icon>新增品項
            </v-btn>
          
    </v-card>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'

export default {
  name: 'item',
  inject: ['reload'],
  data: () => ({
      headers: [
      { title: '品項名稱', field: 'item_name', width: 500, titleAlign: 'center',columnAlign:'center',isEdit:true,
        formatter: function (rowData,rowIndex,pagingIndex,field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`;
        },isResize:true},
      { title: '品項價格', field: 'item_price', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '製作時間', field: 'time', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '售出量', field: 'sales', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:false,componentName:'table-operation',isResize:true }
    ],
    defaultItem: {
      item_name: '品項',
      item_price: '',
      time: '',
      sales: ''
    },
    editedItem: {
      item_name: '品項',
      item_price: '',
      time: '',
      sales: ''
    },
    dataList:[],
    isRouterAlive: true
 
  }),
  methods:{
    customCompFunc(params){
      console.log(params);
      if (params.type === 'delete'){ // do delete operation
        this.$delete(this.dataList,params.index);
      }else if (params.type === 'edit'){ // do edit operation
        alert(`品項名稱：${params.rowData['item_name']}`)
      }
    },
    add () {
      this.dataList.push(this.editedItem)
      this.editedItem = Object.assign({}, this.defaultItem)
      axios.post('http://127.0.0.1:8000/api/accounting/item/',{
                    item_name: '品項',
                    item_price: '',
                    time: '',
                    sales: ''
                    

                })
      this.reload()




    },
    cellEditDone(newValue,oldValue,rowIndex,rowData,field){

                this.dataList[rowIndex][field] = newValue;

                // 接下来处理你的业务逻辑，数据持久化等...
                let params = {type:'edit',index:this.index,rowData:this.rowData};
               this.$emit('on-custom-comp',params);

                axios.put('http://127.0.0.1:8000/api/accounting/item/' + rowData.id + '/',{
                    item_name: this.dataList[rowIndex]['item_name'],
                    item_price: this.dataList[rowIndex]['item_price'],
                    time: this.dataList[rowIndex]['time'],
                    sales: this.dataList[rowIndex]['sales']
                    

                })
                .then(res => console.log(res))
                .catch(err => console.log(err))
                
    
    }
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/api/accounting/item/').then(body => {
      this.dataList = body.data
    })
  }
}
Vue.component('table-operation',{
        template:`<span>
        <a href="" @click.stop.prevent="deleteRow(rowData,index)" style="color:red">刪除</a>
        </span>`,
        props:{
            rowData:{
                type:Object
            },
            field:{
                type:String
            },
            index:{
                type:Number
            }
        },
        methods:{
            deleteRow(rowData, index){

                // 参数根据业务场景随意构造
                
                let params = {type:'delete',index:this.index};
                confirm('確定要刪除此品項?') && this.$emit('on-custom-comp',params);
                axios.delete('http://127.0.0.1:8000/api/accounting/item/' + rowData.id + '/',{
                    data: { username : "root" , password : "ilovelibrary" } 

                })
                .then(res => console.log(res))
                .catch(err => console.log(err))

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
