import { BsArrowRepeat } from "react-icons/bs";
import React from "react";

type RefetchProps = {
  refetch: () => void;
  isRefetching: boolean;
};
const Refetch = ({ refetch, isRefetching }: RefetchProps) => {
  return (
    <div>
      <button className="btn btn-md rounded-2xl" onClick={refetch}>
        <BsArrowRepeat className={isRefetching ? "animate-spin" : ""} />
      </button>
    </div>
  );
};

export default Refetch;
