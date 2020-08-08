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
              <v-icon>mdi-plus</v-icon>新增雜項
            </v-btn>
          
    </v-card>
  </div>
</template>
<script>
import Vue from 'vue'
import axios from 'axios'

export default {
  name: 'misc',
  inject: ['reload'],
  data: () => ({
      headers: [
      { title: '雜項名稱', field: 'miscellaneous_name', width: 300, titleAlign: 'center',columnAlign:'center',isEdit:true,
        formatter: function (rowData,rowIndex,pagingIndex,field) {
          return `<span class='cell-edit-color'>${rowData[field]}</span>`;
        },isResize:true},
      { title: '每月花費', field: 'miscellaneous_price', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '服務作業比例', field: 'service', width: 110, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '料理作業比例', field: 'cooking', width: 110, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '整理管理比例', field: 'sorting', width: 110, titleAlign: 'center',columnAlign:'center',isEdit:true,isResize:true },
      { title: '', field: 'actions', width: 100, titleAlign: 'center',columnAlign:'center',isEdit:false,componentName:'table-operation',isResize:true }
    ],
    defaultItem: {
      miscellaneous_name: '雜項',
      miscellaneous_price: '',
      service: '',
      cooking: '',
      sorting: ''
    },
    editedItem: {
      miscellaneous_name: '雜項',
      miscellaneous_price: '',
      service: '',
      cooking: '',
      sorting: ''
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
        alert(`品項名稱：${params.rowData['miscellaneous_name']}`)
      }
    },
    add () {
      this.dataList.push(this.editedItem)
      this.editedItem = Object.assign({}, this.defaultItem)
      axios.post('http://127.0.0.1:8000/api/accounting/misc/',{
                    miscellaneous_name: '雜項',
                    miscellaneous_price: '',
                    service: '',
                    cooking: '',
                    sorting: ''
                    

                })
      this.reload()




    },
    cellEditDone(newValue,oldValue,rowIndex,rowData,field){

                this.dataList[rowIndex][field] = newValue;
                let params = {type:'edit',index:this.index,rowData:this.rowData};
               this.$emit('on-custom-comp',params);

                axios.put('http://127.0.0.1:8000/api/accounting/misc/' + rowData.id + '/',{
                    miscellaneous_name: this.dataList[rowIndex]['miscellaneous_name'],
                    miscellaneous_price: this.dataList[rowIndex]['miscellaneous_price'],
                    service: this.dataList[rowIndex]['service'],
                    cooking: this.dataList[rowIndex]['cooking'],
                    sorting: this.dataList[rowIndex]['sorting']
                })
                .then(res => console.log(res))
                .catch(err => console.log(err))
                
                
                
    
    }
  },
  mounted() {
    axios.get('http://127.0.0.1:8000/api/accounting/misc/').then(body => {
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
                axios.delete('http://127.0.0.1:8000/api/accounting/misc/' + rowData.id + '/',{
                    data: { username : "root" , password : "ilovelibrary" } 

                })
                .then(res => console.log(res))
                .catch(err => console.log(err))

            }
        }
    })
</script>
<style scoped>
    .cell-edit-color {
        color: #8BC34A;
        font-weight: bold;
    }
</style>
