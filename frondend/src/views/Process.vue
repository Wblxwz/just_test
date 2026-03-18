<template>
    <div style="display: flex;margin-bottom: 1%;">
        <el-button @click="createProcess()" type="primary" style="margin-right: 1%;">创建新监控</el-button>
    </div>
    <el-table border stripe :data="tableData" style="width: 100%">
        <el-table-column v-if="false" prop="id" label="ID" />
        <el-table-column show-overflow-tooltip prop="name" label="名称" />
        <el-table-column show-overflow-tooltip prop="describe" label="描述" />
        <el-table-column show-overflow-tooltip prop="type" label="类型" />
        <el-table-column show-overflow-tooltip prop="args" label="测试IP" />
        <!-- <el-table-column show-overflow-tooltip prop="command" label="测试命令" /> -->
        <el-table-column show-overflow-tooltip prop="status" label="状态" />
        <el-table-column show-overflow-tooltip prop="duration" label="总执行时长" />
        <!-- <el-table-column show-overflow-tooltip prop="elapsed_time" label="已执行时长" />
        <el-table-column show-overflow-tooltip prop="remain_time" label="剩余时长" /> -->
        <el-table-column show-overflow-tooltip prop="start_time" label="开始时间" />
        <el-table-column show-overflow-tooltip prop="end_time" label="结束时间" />
        <!-- <el-table-column show-overflow-tooltip prop="report_url" label="报告地址" /> -->
        <el-table-column label="操作" #default="scope">
          <div style="display: flex;">
            <el-button v-if="scope.row.status === '已完成'" @click="click_view(scope.row)" type="primary">查看</el-button>
            <el-button @click="click_delete(scope.row)" type="danger">删除</el-button>
          </div>
        </el-table-column>
    </el-table>
    <el-dialog v-model="addDialog" style="width: 600px;">
    <el-form :model="processForm" label-width="auto" style="max-width: 600px;margin-top: 5%;">
      <el-form-item label="名称">
        <el-input v-model="processForm.name" />
      </el-form-item>
      <el-form-item label="测试IP">
        <el-input v-model="processForm.host" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input type="textarea" v-model="processForm.describe" />
      </el-form-item>
      <el-form-item label="自定义命令">
        <el-input disabled v-model="processForm.command" />
      </el-form-item>
      <el-form-item label="类型">
        <el-select filterable v-model="processForm.type" placeholder="Select" style="width: 240px">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="脚本说明">
        <el-input v-if="processForm.type === 'JMeter'" disabled v-model="processForm.command" placeholder="使用JMeter进行后端请求压测"/>
      </el-form-item>
      <el-form-item>
        <el-button @click="addProcessButton()" type="success" style="margin-right: 1%;">创建</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog
    v-model="checkViewFlag"
    width="500"
  >
  <div style="display: flex; align-items: center; gap: 20px;">
    <a target="_blank" :href="`http://localhost:8000/${view_report_url}/log/index.html`">报告地址</a>
    <el-button @click="downloadReport" type="success">下载报告</el-button>
  </div>
  </el-dialog>
</template>

<style>

</style>

<script lang="ts" setup>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { onMounted, ref } from 'vue';


interface Process
{
    id?:number,
    name:string,
    describe:string,
    host:string,
    command:string,
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
    value: 'JMeter',
    label: 'JMeter',
  },
  {
    value: 'RobotFramework',
    label: 'RobotFramework',
  },
  {
    value: 'Pytest',
    label: 'Pytest',
  },
]
const tableData = ref<Process[]>([])
const processForm = ref<Process>({} as Process)
onMounted(async ()=>{
    const response = await axios.get("http://127.0.0.1:8000/process")
    tableData.value = response.data
})
const addDialog = ref(false)
const checkViewFlag = ref(false)
const createProcess = ()=>{
    processForm.value.name = ""
    processForm.value.host = ""
    processForm.value.describe = ""
    processForm.value.type = ""
    addDialog.value = true
}
const addProcessButton = async ()=>{
  console.log(processForm.value)
  const args = ref("")
  switch (processForm.value.type)
  {
    case "JMeter":
      args.value = "host:" + processForm.value.host
      break;
  }
  const process_json = {
    "name":processForm.value.name,
    "describe":processForm.value.describe,
    "type":processForm.value.type,
    "args":args.value
  }
  const response = await axios.post("http://127.0.0.1:8000/process",process_json)
  if (response.data.ok)
  {
    ElMessage.success("创建成功")
  }
  else
  {
    ElMessage.success("创建失败")
  }
  addDialog.value = false
  const response_get = await axios.get("http://127.0.0.1:8000/process")
  tableData.value = response_get.data
}

const view_report_url = ref("")
const row_id = ref()
const click_view = async (row:Process)=>{
  console.log(row)
  view_report_url.value = row.report_url.slice(row.report_url.indexOf("reports"))
  row_id.value = row.id
  checkViewFlag.value = true
}
const click_delete = async (row:Process)=>{
  console.log(row)
  const response = await axios.delete("http://127.0.0.1:8000/process/" + row.id)
  if (response.data.ok)
  {
    ElMessage.success("删除成功")
  }
  else
  {
    ElMessage.success("删除失败")
  }
  const response_get = await axios.get("http://127.0.0.1:8000/process")
  tableData.value = response_get.data
}
const downloadReport = ()=>{
  const downloadLink = "http://127.0.0.1:8000/process/url/" + row_id.value
  const link = document.createElement("a")
  link.href = downloadLink
  // link.download = data.name
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

</script>