<template>
<el-tree
    style="max-width: 100%"
    :props="props"
    :load="loadNode"
    lazy
  />    
</template>

<script setup>

const props = {
  label: 'name',
  isLeaf: 'leaf',
}
const loadNode = (node, resolve)=>
{
    if (node.level === 0) {
    return resolve([{ name: 'main' }])
  }
  if (node.level > 1) return resolve([])

  setTimeout(() => {
    const data = [
      {
        name: 'leaf',
        leaf: true,
      },
      {
        name: 'zone',
        leaf: true,
      },
    ]

    resolve(data)
  }, 500)
}
</script>
