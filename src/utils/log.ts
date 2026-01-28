import {TVersionObject} from "@/utils/type.ts";

export const CHANGELOG_LIST: Array<TVersionObject> = [
  {
    version: '1.0.0',
    date: '1150128',
    logs: [
      {color: "new", text: '完成比對工作紀錄簿及日誌的功能'},
    ]
  }
]

export const AppVersion = CHANGELOG_LIST[0].version
export const AppVersionText = `${CHANGELOG_LIST[0].version}（${CHANGELOG_LIST[0].date}）`