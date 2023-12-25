 import useAxios from "../hooks/useAxios"
 
 const endpoint = useAxios()
 export const getGros = async (params:any) => {

    try{
       return endpoint.get("http://localhost:8000/api/container/gros/", {params: {...params}})
    }catch(error){
        console.log(error)
    }
}