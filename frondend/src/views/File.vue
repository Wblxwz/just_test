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
            <el-button type="success" link @click.stop="download(data)">
              下载
            </el-button>
            <el-button
              type="danger"
              link
              @click.stop="remove(node, data)"
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
        ref="folderUpload"
        v-if="fileForm.type === 'folderRadio'"
        v-model:file-list="folderList"
        class="upload-demo"
        action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
        :auto-upload=false
        multiple
        directory
        :before-upload="beforeUpload"
      >
        <el-button type="primary">点击选择文件夹</el-button>
        </el-upload>
        <el-upload
          ref="fileUpload"
          v-if="fileForm.type === 'fileRadio'"
          v-model:file-list="fileList"
          class="upload-demo"
          action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
          :auto-upload=false
          multiple
          :limit="1"
          :on-exceed="handleExceed"
          :before-upload="beforeUpload"
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

<script setup>
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { ref, watch } from 'vue'

const fileUpload = ref(null)
const folderUpload = ref(null)
const fileList = ref([])
const folderList = ref([])
const fileForm = ref({
  name: '',
  type: 'folderRadio',
})
const props = {
  label: 'name',
  isLeaf: 'leaf',
}
const loadNode = (node, resolve)=>
{
  if (node.level === 0) {
    axios.get("http://127.0.0.1:8000/file").then((response)=>{
    const files = response.data
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
const remove = (node, data)=>
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
const myNode = ref(null)
const myData = ref(null)
const myFileSize = ref(null)
const append = (node = null,data = null)=>{
  addDialog.value = true
  fileForm.value.name = ""
  fileForm.value.type = "folderRadio"
  myNode.value = node
  myData.value = data
  fileList.value = []
  folderList.value = []
}
const addFileButton = ()=>{
  let leaf = false
  if (fileForm.value.type === "fileRadio")
  {
    leaf = true
    fileUpload.value.submit()
    // console.log(fileList.value[0].size)
  }
  else{
    folderUpload.value.submit()
  }
  const json = {
    "name":fileForm.value.name,
    "leaf":leaf,
    "parent_id":myNode.value ? myNode.value.data.id : 0,
    "file_size": Math.ceil(myFileSize.value / 1024) + "kb",
    "url":"123"
    }
    axios.post("http://127.0.0.1:8000/file",json).then((response)=>{
    addDialog.value = false
    if (response.data.ok === true)
    {
      ElMessage.success("新建成功")
      if (fileForm.value.type === "folderRadio" && folderList.value.length != 0)
      {
        const json_list = ref([])
        console.log(folderList.value.length)
        for(let i=0;i < folderList.value.length;i++)
        {
          const json = {
          "name":folderList.value[i].raw.name,
          //文件夹上传时会被扁平化处理
          "leaf":true,
          "parent_id":response.data.file.id,
          "file_size": Math.ceil(folderList.value[i].raw.size / 1024) + "kb",
          "url":"123"
          }
          json_list.value.push(json)
        }
        axios.post("http://127.0.0.1:8000/file/folder",json_list.value).then((response)=>{
          if (response.data.ok === true)
          {
            ElMessage.success("上传文件夹成功")
          }
          else
          {
            ElMessage.error("上传文件夹失败")
          }
        })
      }
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
const filterNode = (value,data)=>{
  if (!value) return true
  return data.name.includes(value)
}
const treeRef = ref(null)
watch(filterText, (val) => {
  // 核心：先校验 treeRef.value 存在，再执行 filter
  if (treeRef.value && typeof treeRef.value.filter === 'function') {
    treeRef.value.filter(val)
  }
})
const beforeUpload = (rawFile)=>{
  myFileSize.value += rawFile.size
  return true
}
const handleExceed = ()=>{
  ElMessage("最多可上传一个文件")
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