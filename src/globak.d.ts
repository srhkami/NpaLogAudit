import {
  FilesForm,
  Response,
} from "./utils/type.ts";

export {};

/* 自訂的全局類別，用來定義API接口格式 */
declare global {
  interface Window {
    pywebview: {
      api: {
        start(data: { shiftPath: string, logPath: string }): Promise,
        select_excel(): Promise<Response<{ path: string }>>,
      },
      updateProgress: (progress: number) => void,
    }
  }
}