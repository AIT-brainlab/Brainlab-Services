const restAPIGet = async(path:string, onFailure?:(resp:Response)=>void ):Promise<any> => {
    const resp:Response = await fetch(path, { method: "GET" })
    if (resp.status === 200) {
        const jsonData = await resp.json()
        return jsonData
    } else {
        if(onFailure!=undefined){
            onFailure(resp)
        }else{
            let jsonData = await resp.json()
            return {...jsonData,...{status:resp.status}}
        
        }
    }
}

const restAPIMethod = async(path:string, method:string, body:any, onSuccess:(jsonData:any) => void, onFailure:(resp:Response) => void) => {
    const resp = await fetch(path, {
        method,
        headers: {
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify(body)
    })
    if (resp.status === 200) {
        const jsonData = await resp.json()
        onSuccess(jsonData)
    } else {
        onFailure(resp)
    }
}
const restAPIPost = async(path:string, body:any, onSuccess:(jsonData:any) => void, onFailure:(resp:Response) => void):Promise<any> => {
    await restAPIMethod(path, "POST", body, onSuccess, onFailure)
}
export { restAPIGet, restAPIMethod }