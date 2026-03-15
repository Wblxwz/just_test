<template>
    <div style="display: flex;margin-bottom: 1%;">
        <el-button @click="createProcess()" type="primary" style="margin-right: 1%;">创建新监控</el-button>
    </div>
    <el-table stripe :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="ID" />
        <el-table-column show-overflow-tooltip prop="name" label="名称" />
        <el-table-column show-overflow-tooltip prop="describe" label="描述" />
        <el-table-column show-overflow-tooltip prop="type" label="类型" />
        <el-table-column show-overflow-tooltip prop="status" label="状态" />
        <el-table-column show-overflow-tooltip prop="duration" label="预计时长" />
        <el-table-column show-overflow-tooltip prop="remain_time" label="剩余时长" />
        <el-table-column show-overflow-tooltip prop="start_time" label="开始时间" />
        <el-table-column show-overflow-tooltip prop="end_time" label="结束时间" />
        <el-table-column show-overflow-tooltip prop="report_url" label="报告地址" />
    </el-table>
    <el-dialog v-model="addDialog" style="width: 600px;">
    <el-form :model="processForm" label-width="auto" style="max-width: 600px;margin-top: 5%;">
      <el-form-item label="名称">
        <el-input v-model="processForm.name" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input type="textarea" v-model="processForm.describe" />
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="processForm.type" placeholder="Select" style="width: 240px">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button @click="addProcessButton()" type="success" style="margin-right: 1%;">新建</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<style>

</style>

<script lang="ts" setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';


interface Process
{
    id?:number,
    name:string,
    describe:string,
    start_time:string | number,
    end_time:string | number,
    report_url:string,
    duration:string | number,
    type:string,
    status:string,
    remain_time:string | number
}
const options = [
{
    value: 'Option1',
    label: 'Option1',
  },
  {
    value: 'Option2',
    label: 'Option2',
  },
  {
    value: 'Option3',
    label: 'Option3',
  },
  {
    value: 'Option4',
    label: 'Option4',
  },
  {
    value: 'Option5',
    label: 'Option5',
  },
]
const tableData = ref<Process[]>([])
const processForm = ref<Process>({} as Process)
onMounted(async ()=>{
    const response = await axios.get("http://127.0.0.1:8000/process")
    tableData.value = response.data
})
const addDialog = ref(false)
const createProcess = ()=>{
    addDialog.value = true
}
const addProcessButton = ()=>{

}

</script>