<template>
  <div style="display: flex;margin-bottom: 1%;">
    <el-button @click="append()" type="primary" style="margin-right: 1%;">新建</el-button>
    <el-input
    v-model="filterText"
    class="w-60 mb-2"
    placeholder="Filter keyword"
    />
  </div>
<el-tree
    style="max-width: 100%"
    :props="props"
    :load="loadNode"
    lazy
    ref="treeRef"
    node-key="id"
    :filter-node-method="filterNode"
  >
  <template #default="{ node, data }">
    <el-tag style="margin-right: 2%;" type="primary">{{ data.leaf ? "文件" : "文件夹"}}</el-tag>
    <el-tag style="margin-right: 2%;" v-if="data.leaf ? true : false" type="success">{{ data.file_size }}</el-tag>
        <div class="custom-tree-node">
          <span>{{ node.label }}</span>
          <div>
            <el-button type="primary" link @click.stop="append(node,data)" v-if="!data.leaf">
              新建
            </el-button>
            <el-button type="success" link @click.stop="download(data)" v-if="data.leaf">
              下载
            </el-button>
            <el-button
              type="danger"
              link
              @click.stop="remove(node,data)"
            >
              删除
            </el-button>
          </div>
        </div>
      </template>
  </el-tree>
  <el-dialog v-model="addDialog" style="width: 600px;">
    <el-form :model="fileForm" label-width="auto" style="max-width: 600px;margin-top: 5%;">
      <el-form-item label="名称">
        <el-input v-model="fileForm.name" />
      </el-form-item>
      <el-form-item label="类型">
        <el-radio-group v-model="fileForm.type">
          <el-radio value="folderRadio" size="large">文件夹</el-radio>
          <el-radio value="fileRadio" size="large">文件</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item>
        <el-upload
          ref="fileUpload"
          v-if="fileForm.type === 'fileRadio'"
          v-model:file-list="fileList"
          class="upload-demo"
          :auto-upload=false
          multiple
          :limit="1"
          :on-exceed="handleExceed"
          :on-change="fileChange"
        >
          <el-button type="primary">点击选择文件</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item>
        <el-button @click="addFileButton()" type="success" style="margin-right: 1%;">新建</el-button>
      </el-form-item>      
    </el-form>
  </el-dialog>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref, watch } from 'vue'
import type {
  LoadFunction,
  FilterNodeMethodFunction,
  RenderContentContext,
  RenderContentFunction,
  TreeInstance,
  UploadProps, UploadUserFile,UploadFiles,UploadFile
} from 'element-plus'

interface Tree {
  [key: string]: any
}
interface FileNode{
  id?:number,
  name:string,
  leaf:boolean,
  parent_id:number,
  file_size:string,
  url:string
}
type Node = RenderContentContext['node']
type Data = RenderContentContext['data']

const fileSize = ref()
const fileList = ref<UploadUserFile[]>([])
const folderList = ref<UploadUserFile[]>([])
const fileForm = ref({
  name: '',
  type: 'folderRadio',
})
const props = {
  label: 'name',
  isLeaf: 'leaf',
}
const loadNode:LoadFunction = (node, resolve)=>
{
  if (node.level === 0) {
    axios.get("http://127.0.0.1:8000/file").then((response)=>{
    const files:FileNode[] = response.data
    const folderNodes = files.filter(item => item.parent_id === 0)
    resolve(folderNodes)
    })
  }
  else
  {
    setTimeout(() => {
    axios.get("http://127.0.0.1:8000/file/folder/" + node.data.id).then((response)=>{
      const files = response.data
      resolve(files)
    })
  }, 500)
  }
}
const remove = (node: Node, data: Data)=>
{
  axios.delete("http://127.0.0.1:8000/file/folder/" + node.data.id).then((response)=>{
    if (response.data.ok === true)
    {
      ElMessage.success("删除成功")
    }
    else
    {
      ElMessage.error("删除失败")
    }
    const parentNode = node.parent
    if (parentNode)
    {
      parentNode.loaded = false
      parentNode.expand()
    }
  })
}
const addDialog = ref(false)
const myNode = ref()
const myData = ref()
const myFileSize = ref()
const append = (node = null,data = null)=>{
  addDialog.value = true
  fileForm.value.name = ""
  fileForm.value.type = "folderRadio"
  myNode.value = node
  myData.value = data
  fileList.value = []
  folderList.value = []
}
const addFileButton = async ()=>{
  let leaf = false
  let fileName = ""
  leaf = true
  const formData = new FormData()
  if (fileForm.value.type === "fileRadio")
  {
    formData.append("file",fileList.value[0]?.raw!)
    const response = await axios.post("http://127.0.0.1:8000/file/upload",formData)
    fileName = response.data.file
  }
  else
  {
    leaf = false
  }
  const json = {
    "name":fileForm.value.name,
    "leaf":leaf,
    "parent_id":myNode.value ? myNode.value.data.id : 0,
    "file_size": Math.ceil(fileSize.value / 1024) + "kb",
    "url":fileName ? fileName : "folder"
    }
    axios.post("http://127.0.0.1:8000/file",json).then((response)=>{
    addDialog.value = false
    if (response.data.ok === true)
    {
      ElMessage.success("新建成功")
    }
    else
    {
      ElMessage.error("新建失败")
    }
    const parentNode = myNode.value ? myNode.value.parent : null
    if (parentNode)
    {
      parentNode.loaded = false
      parentNode.expand()
    }
    else
    {
      window.location.reload()
    }
    })
}
const filterText = ref('')
const filterNode:FilterNodeMethodFunction  = (value:string,data:Tree)=>{
  if (!value) return true
  return data.name.includes(value)
}
const treeRef = ref()
watch(filterText, (val) => {
  // 核心：先校验 treeRef.value 存在，再执行 filter
  if (treeRef.value && typeof treeRef.value.filter === 'function') {
    treeRef.value.filter(val)
  }
})
const handleExceed:() => void = ()=>{
  ElMessage("最多可上传一个文件")
}
const download = (data:FileNode)=>{
  const downloadLink = "http://127.0.0.1:8000/file/download/" + data.id
  const link = document.createElement("a")
  link.href = downloadLink
  link.download = data.name
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
const fileChange = (uploadFile: UploadFile, uploadFiles: UploadFiles)=>{
  fileSize.value = uploadFile.size
}
</script>
<style>
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
  height: 26px; /* 与 --el-tree-node-content-height 保持一致 */
  line-height: 26px;
  overflow: hidden;
}
</style>