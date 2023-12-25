import React, {useState, useEffect} from "react";
import { Button, Modal } from "antd";
import {useQuery} from '@tanstack/react-query'
import { getGros } from "../api/endpoints";

const PrestationsConteneur = () => {

  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const d = {
    page_size : 30, 
    expand:'regime',
    regime__designation__exact: "D1"
  }

  const {data, isLoading, isError} = useQuery({ queryKey: ['gros'], queryFn: () => getGros(d) })


  return (
    <div>
      <Button type="primary" className="bg-primary hover:bg-green-800  dark:bg-base-200 dark:hover:bg-gray-800 m-20" onClick={showModal}>
        Open Modal
      </Button>
      <Modal
        title="Basic Modal"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        okButtonProps={{className:"bg-primary hover:bg-green-800 text-white dark:bg-base-200 dark:hover:bg-gray-800"}}
      >
        <p>Some contents...</p>
        <p>Some contents...</p>
        <p>Some contents...</p>
      </Modal>
    </div>
  );
};

export default PrestationsConteneur;
