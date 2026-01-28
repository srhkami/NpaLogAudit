import {Badge, Button, Loading} from "@/component";
import {useState} from "react";
import toast from "react-hot-toast";
import {FaCircleCheck, FaFileCirclePlus} from "react-icons/fa6";
import {FaSearchPlus} from "react-icons/fa";
import {showToast} from "@/utils/handleToast.ts";

export default function Upload() {

  const [shiftPath, setShiftPath] = useState<string>();
  const [logPath, setLogPath] = useState<string>();
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const onSelectFile = (mode: 'shift' | 'log') => {
    window.pywebview.api.select_excel()
      .then((res) => {
        if (mode == 'shift') {
          if (!res.data.path.includes('工作紀錄簿')) {
            toast.error('檔名應包含「工作紀錄簿」！')
            return
          }
          setShiftPath(res.data.path);
        } else {
          if (!res.data.path.includes('稽核調閱')) {
            toast.error('檔名應包含「稽核調閱」！')
            return
          }
          setLogPath(res.data.path);
        }
      })
      .catch(err => {
        toast.error(err.toString())
        if (mode == 'shift') {
          setShiftPath(undefined)
        } else {
          setLogPath(undefined)
        }
      })

  }

  const onSubmit = () => {
    setIsLoading(true);
    showToast(
      async () =>
        await window.pywebview.api.start({
          shiftPath: shiftPath ?? '',
          logPath: logPath ?? '',
        })
      ,
      {
        baseText: '處理', success: '儲存成功'
      }
    )
      .finally(() => setIsLoading(false))
  }

  return (
    <div>
      <div className='flex items-center justify-center'><Badge color='accent'>Step 1</Badge></div>
      <div className='text-lg font-bold flex justify-center items-center my-2'>
        請選擇「工作記錄簿」Excel檔
      </div>
      <div className='text-sm text-center italic my-2 opacity-50'>
        請注意系統單次查詢上限為1000筆，如果單月超過上限務必分別匯出檔案，逐一比對！
      </div>
      <div className='flex justify-center items-center my-2 join'>
        <Button name='shiftBtn' size='sm'
                color={shiftPath ? 'success' : 'primary'}
                className='join-item'
                onClick={() => onSelectFile('shift')}>

          {shiftPath ? <FaCircleCheck/> : <FaFileCirclePlus/>}
          選擇檔案
        </Button>
      </div>
      <div className='divider my-1'/>

      <div className='flex items-center justify-center'><Badge color='accent'>Step 2</Badge></div>
      <div className='text-lg font-bold flex justify-center items-center my-2'>
        請選擇「主管稽核調閱」Excel檔
      </div>
      <div className='text-sm text-center italic my-2 opacity-50'>
        一般系統及M-Police皆有支援
      </div>
      <div className='flex justify-center items-center my-2'>
        <Button name='shiftBtn' size='sm'
                color={logPath ? 'success' : 'primary'}
                className='join-item'
                onClick={() => onSelectFile('log')}>
          {logPath ? <FaCircleCheck/> : <FaFileCirclePlus/>}
          選擇檔案
        </Button>
      </div>
      <div className='divider my-1'/>
      <div className='my-2'>
        {isLoading ?
          <div className='flex items-center justify-center p-2'>
            <Loading style='bars'/>
          </div>
          :
          <Button color='primary' shape='block'
                  disabled={!logPath || !shiftPath} onClick={onSubmit}>
            <FaSearchPlus/>開始比對
          </Button>
        }
      </div>
    </div>
  )
}