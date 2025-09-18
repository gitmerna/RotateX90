bl_info = {
    "name": "_ Unity. X Rotation Adjust",
    "author": "Yame",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Rotate Tools",
    "description": "Adjust X rotation: -90, apply transform, +90",
    "category": "3D View",
}

import bpy
import math

# --- オペレーター ---
class OBJECT_OT_XRotationAdjust(bpy.types.Operator):
    bl_idname = "object.x_rotation_adjust"
    bl_label = "Adjust X Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            # 現在のX回転（ラジアン）
            x_rot = obj.rotation_euler[0]
            
            # Xが90°(π/2ラジアン)なら処理しない
            if math.isclose(x_rot % (2*math.pi), math.pi/2, abs_tol=1e-5):
                continue

            # 1. Xを-90°回転
            obj.rotation_euler[0] -= math.radians(90)

            # 2. Transformの回転を適用
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.transform_apply(rotation=True)

            # 3. Xを+90°回転
            obj.rotation_euler[0] += math.radians(90)

        return {'FINISHED'}


# --- パネル ---
class VIEW3D_PT_XRotationAdjustPanel(bpy.types.Panel):
    bl_label = "Rotate Tools"
    bl_idname = "VIEW3D_PT_x_rotation_adjust_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rotate Tools"

    def draw(self, context):
        layout = self.layout
        show_button = False
        has_object = False

        layout.label(text="Unity用にX90度の回転を行います")

        # 選択オブジェクトのX回転をチェック
        for obj in context.selected_objects:
            has_object = True
            # Xが90°(π/2ラジアン)でないオブジェクトが1つでもあれば表示
            if not math.isclose(obj.rotation_euler[0] % (2*math.pi), math.pi/2, abs_tol=1e-5):
                show_button = True
                break

        if show_button:
            layout.operator("object.x_rotation_adjust", text="Adjust X Rotation")
        else:
            if has_object:
                layout.label(text="既に回転済みです", icon='INFO_LARGE')
            else:
                layout.label(text="オブジェクトが選択されてません", icon='WARNING_LARGE')


# --- register/unregister ---
classes = [OBJECT_OT_XRotationAdjust, VIEW3D_PT_XRotationAdjustPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
