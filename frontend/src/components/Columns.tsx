import React, { Children, useEffect, useState } from 'react'
import { GROS_COLUMNS } from '../routes/gros/data'
import { Button, Drawer, Modal, Tree } from 'antd';
import { RiSettings4Line } from "react-icons/ri";

type ColumnsProps = {
    COLUMNS:string[]
}

type treeItemType = {
  title : string, 
  key: string, 
  checked: boolean,
  children?: treeItemType[] 
}



const Columns = () => {
  const [cols, setCols] =  useState<treeItemType[]>([])
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let schema:treeItemType[] = []
    GROS_COLUMNS.map(item => {
        if (item.schema.length > -1){
          schema.push({
            'title': item.dataIndex, 
            'key': item.key, 
            'checked': item.checked
          })
        }
            
    })
    setCols(schema)
  }, [])

 const onClose = () => {
  setOpen(false)
 }
  return (
    <>

      <button className="btn btn-md rounded-2xl" onClick={() => setOpen(true)}>
        <RiSettings4Line />
      </button>
      <Drawer title="Settings" placement="right" onClose={onClose} open={open}>
        <div className='py-[10px]'></div>
      <Tree
      showLine={true}
      className='overflow-y-auto max-h-[80vh]'
      checkable
      defaultCheckedKeys={cols.filter(item => item.checked).map(item => item.key)}
      treeData={cols}
    />
      </Drawer>
    </>
  )
}

export default Columns