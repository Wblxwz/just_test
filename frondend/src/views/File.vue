<template>
<el-tree
    style="max-width: 100%"
    :props="props"
    :load="loadNode"
    node-key="id"
    lazy
  >
  <template #default="{ node, data }">
        <div class="custom-tree-node">
          <span>{{ node.label }}</span>
          <span>{{ data.file_size }} </span>
          <div>
            <el-button type="primary" link @click="append(data)">
              添加
            </el-button>
            <el-button type="success" link @click="download(data)">
              下载
            </el-button>
            <el-button
              type="danger"
              link
              @click="remove(node, data)"
            >
              删除
            </el-button>
          </div>
        </div>
      </template>
  </el-tree>
</template>

<script setup>
import axios from 'axios'

const props = {
  label: 'name',
  isLeaf: 'leaf',
}

const loadNode = (node, resolve)=>
{
  if (node.level === 0) {
    axios.get("http://127.0.0.1:8000/file").then((response)=>{
    const files = response.data
    const folderNodes = files.filter(item => item.leaf === false && item.parent_id === 0)
    resolve(folderNodes)
    })
  }

  setTimeout(() => {
    axios.get("http://127.0.0.1:8000/file/folder/" + node.data.id).then((response)=>{
      const files = response.data
      resolve(files)
    })
  }, 500)
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