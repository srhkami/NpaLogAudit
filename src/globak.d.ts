import {AppConfig, Response} from "./utils/type.ts";


/* 自訂的全局類別，用來定義API接口格式 */
declare global {
  interface Window {
    pywebview: {
      api: {
        start(data: { shiftPath: string, logPath: string }): Promise,
        select_excel(): Promise<Response<{ path: string }>>,
        get_config(): Promise<Response<AppConfig>>,
        save_config(key: keyof AppConfig, value: string): Promise,
      },
      updateProgress: (progress: number) => void,
    }
  }
}