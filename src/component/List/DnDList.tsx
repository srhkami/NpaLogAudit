import {
  DndContext, //拖曳邏輯的根元件，提供拖曳事件管理
  closestCenter, //拖曳碰撞判斷邏輯，以 item 中心點距離最近 來決定放置位置
  useSensor, // 設定拖曳的「感應方式」，可混用滑鼠、鍵盤、觸控
  useSensors,
  TouchSensor, // 負責「 觸控」啟用拖曳的感應器
  MouseSensor, // 負責「滑鼠」啟用拖曳的感應器
  DragEndEvent // 拖曳事件的類型
} from '@dnd-kit/core'
import {
  arrayMove, //用來對陣列中的項目重新排序
  SortableContext, //告訴 DnD Kit：這些項目是可以排序的集合，接收的 items 是 item 的 id 陣列（順序會影響排序結果）
  verticalListSortingStrategy //使用「垂直排序策略」，適合清單類 UI
} from '@dnd-kit/sortable'
import {
  restrictToVerticalAxis, //僅允許上下拖曳
  restrictToWindowEdges //拖曳時不允許超出視窗邊界
} from '@dnd-kit/modifiers'
import {Dispatch, HTMLAttributes, SetStateAction} from 'react'
import {twMerge} from "tailwind-merge";

type Props<T> = {
  items: Array<{ id: string | number } & T>
  setItems: Dispatch<SetStateAction<Array<{ id: string | number} & T>>>
}

/**
 * 可以拖曳的列表組件
 * @param children 子組件，應為DnDListItem
 * @param items 項目列表的State，需包含「id」欄位
 * @param setItems 設定項目列表State的函數
 * @param className
 * @constructor
 */
export default function DnDList<T>({
                                     children,
                                     items,
                                     setItems,
                                     className,
                                   }: Props<T> & HTMLAttributes<HTMLUListElement>) {

  const sensors = useSensors(
    useSensor(MouseSensor, {
      activationConstraint: {
        distance: 5, // 防誤觸
      },
    }),
    useSensor(TouchSensor, {
      activationConstraint: {
        delay: 150,
        tolerance: 5,
      },
    })
  )

  // 拖曳完成時更新排序
  const handleDragEnd = (event: DragEndEvent) => {
    const {active, over} = event
    if (!over || active.id === over.id) return;

    const oldIndex = items.findIndex(item => item.id === active.id)
    const newIndex = items.findIndex(item => item.id === over.id)

    if (oldIndex !== -1 && newIndex !== -1) {
      setItems(prev => arrayMove(prev, oldIndex, newIndex));
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
      modifiers={[restrictToVerticalAxis, restrictToWindowEdges]}
    >
      <SortableContext
        items={items.map(item => item.id)}
        strategy={verticalListSortingStrategy}
      >
        <ul className={twMerge('list', className)}>
          {children}
        </ul>
      </SortableContext>
    </DndContext>
  )
}