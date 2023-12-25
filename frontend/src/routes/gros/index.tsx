import { useState } from "react";
import { Table } from "antd";
import { getGros } from "./api";
import { useQuery } from "@tanstack/react-query";
import { GROS_COLUMNS, BREADCRUMBS } from "./data";
import { PaginationProps } from "antd";
import Breadcrumbs from "../../components/Breadcrumbs";
import Refetch from "../../components/Refetch";
import Columns from "../../components/Columns";

const Gros = () => {
  const [pageSize, setPageSize] = useState(400);
  const [page, setPage] = useState(1);

  let to_expand:string[] = []
  let fields:string[] = []
  GROS_COLUMNS.map(item => {
    if(item.checked && item.expand){
      to_expand.push(item.expand)
      fields.push(item.expand)

    }else{
      if(item.checked){
        fields.push(item.dataIndex);
      }
    }

  })
  
  const attr = {
    page_size: pageSize,
    page: page,
    //expand: "gros,port_reception,navire,consignataire,regime,port_emission",
    expand: to_expand.join(','), 
    fields: fields
  };

  const { refetch, data, isLoading, isRefetching } = useQuery({
    queryKey: ["gros", attr],
    queryFn: () => getGros(attr),
  });
  const handlePaginationChange: PaginationProps['onShowSizeChange'] = (current, pageSize) => {
    setPage(current);
    setPageSize(pageSize);
    refetch();
  };
  console.log(data);
  const handleChange = (pagination: PaginationProps) => {};
  return (
    <div className="p-[20px] mt-[60px] static">
       <Breadcrumbs data={BREADCRUMBS} />
      <div className="h-[70px] flex justify-end gap-2">
        <Columns />
        <Refetch refetch={refetch} isRefetching={isRefetching} />
      </div>
      <div >
        <Table
        className="w-[85vw]"
          scroll={{ x: 1500, y: "70vh" }}
          size="small"
          pagination={{
            pageSize: pageSize,
            total: data?.data?.count,
            current: page,
            onChange: handlePaginationChange,
            showSizeChanger: true,
            showQuickJumper: true,
            position: ["bottomCenter"],
          }}
          columns={GROS_COLUMNS.filter(item => item.checked)}
          dataSource={data?.data?.results}
          loading={isLoading}
          onChange={handleChange}
        />
      </div>
    </div>
  );
};

export default Gros;
