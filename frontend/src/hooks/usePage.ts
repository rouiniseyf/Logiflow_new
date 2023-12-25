const usePage = () => {
  let page_size: string | null = localStorage.getItem("page_size");

  const setPageSize = (page_size: number) => {
    localStorage.setItem("page_size", page_size.toString());
  };

  const getPageSize = () => {
    if (page_size) {
      return parseInt(page_size);
    }
    return 10;
  };

  return {getPageSize, setPageSize};
};

export default usePage;
