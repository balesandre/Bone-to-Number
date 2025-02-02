bl_info = {
    "name": "Bone to Number",
    "blender": (4, 0, 0),
    "category": "3D view",
    "version": (1, 0),
    "author": "André Bales",
    "wiki_url": "https://github.com/balesandre/Bone-to-Number",
    "description": "Ferramentas para criar e manipular textos numéricos no Blender.",
}

import bpy

# Função para criar números
def create_numbers():
    bpy.ops.object.text_add()
    obj = bpy.context.object
    obj.data.body = "0123456789"
    obj.data.align_x = 'CENTER'

# Operador para criar números
class UX_RIG_OT_create_numbers(bpy.types.Operator):
    bl_idname = "ux_rig.create_numbers"
    bl_label = "Create Numbers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        create_numbers()
        return {'FINISHED'}

# Operador para escolher a fonte
class UX_RIG_OT_choose_font(bpy.types.Operator):
    bl_idname = "ux_rig.choose_font"
    bl_label = "Choose the Font"
    bl_options = {'REGISTER', 'UNDO'}
    
    filter_glob: bpy.props.StringProperty(
        default='*.ttf;*.otf',  # Font file types
        options={'HIDDEN'}
    )
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        if context.object and context.object.type == 'FONT':
            context.object.data.font = bpy.data.fonts.load(self.filepath)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Função para executar o script "Make UX"
def make_ux():
    # Verifica se há um objeto de texto selecionado e obtém a fonte
    selected_obj = bpy.context.object
    if selected_obj is None or selected_obj.type != 'FONT':
        print("Selecione um objeto de texto para definir a fonte.")
        return

    font = selected_obj.data.font

    # Função para adicionar objetos de texto numerados
    def adicionar_texto_numerado(numero, nome):
        bpy.ops.object.text_add()
        obj = bpy.context.object
        obj.data.body = str(numero)
        obj.data.align_x = 'CENTER'
        obj.name = nome
        obj.data.font = font  # Aplica a fonte escolhida
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

    # Lista de números e seus respectivos nomes
    numeros_nomes = [
        (0, "Zero"),
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
        (5, "Five"),
        (6, "Six"),
        (7, "Seven"),
        (8, "Eight"),
        (9, "Nine")
    ]

    # Desmarca todos os objetos
    bpy.ops.object.select_all(action='DESELECT')

    # Adiciona cada objeto de texto numerado e os seleciona
    for numero, nome in numeros_nomes:
        adicionar_texto_numerado(numero, nome)

    print("Objetos de texto numerados de 0 a 9 adicionados ao mundo, alinhados ao centro horizontalmente, renomeados e todos selecionados.")

    # Lista de nomes dos objetos que queremos selecionar
    nomes_dos_objetos = [
        "Zero",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine"
    ]

    # Desmarca todos os objetos
    bpy.ops.object.select_all(action='DESELECT')

    # Seleciona os objetos pelos nomes fornecidos
    for nome in nomes_dos_objetos:
        if nome in bpy.data.objects:
            bpy.data.objects[nome].select_set(True)
            bpy.context.view_layer.objects.active = bpy.data.objects[nome]

    print("Objetos nomeados de Zero a Nine selecionados.")

    # Seleciona o objeto de texto ativo
    obj = bpy.context.object

    # Verifica se o objeto é do tipo 'FONT'
    if obj.type == 'FONT':
        # Converte o texto em mesh
        bpy.ops.object.convert(target='MESH')
        print("Texto convertido em mesh com sucesso.")
    else:
        print("Selecione um objeto de texto.")

    def adicionar_grupo_vertices_com_pintura(obj):
        if obj.type != 'MESH':
            print(f"O objeto {obj.name} não é do tipo MESH.")
            return

        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        if obj.vertex_groups.get(obj.name):
            grupo = obj.vertex_groups[obj.name]
        else:
            grupo = obj.vertex_groups.new(name=obj.name)

        for v in obj.data.vertices:
            grupo.add([v.index], weight=1.0, type='REPLACE')

        print(f"Grupo de vértices '{obj.name}' adicionado ao objeto {obj.name} com peso 1.0.")
        bpy.ops.object.mode_set(mode='EDIT')

    for obj in bpy.context.selected_objects:
        adicionar_grupo_vertices_com_pintura(obj)

    print("Grupos de vértices adicionados e pintados em 1.0 para todos os objetos selecionados.")

    bpy.ops.object.editmode_toggle()

    if bpy.context.selected_objects:
        bpy.ops.object.join()
        if bpy.context.object:
            bpy.context.object.name = "Numbers"
        print("Todos os objetos selecionados foram juntados em um único objeto chamado 'Numbers'.")
    else:
        print("Nenhum objeto selecionado para juntar.")

    bpy.ops.object.editmode_toggle()

    obj = bpy.context.object
    if obj is None or obj.type != 'MESH':
        print("Selecione um objeto do tipo 'MESH'")
    else:
        vertex_groups = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]

        for group_name in vertex_groups:
            if group_name in obj.vertex_groups:
                mask_modifier = obj.modifiers.new(name=f"Mask_{group_name}", type='MASK')
                mask_modifier.vertex_group = group_name
            else:
                print(f"O grupo de vértices '{group_name}' não existe no objeto '{obj.name}'")

    print("Modificadores Mask adicionados com sucesso!")

    selected_obj = bpy.context.active_object
    if selected_obj is None:
        print("Selecione um objeto.")
    else:
        bpy.ops.object.mode_set(mode='OBJECT')
        location = selected_obj.location
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=location)
        empty_obj = bpy.context.object
        empty_obj.name = "Number_control"
        empty_obj.empty_display_type = 'SINGLE_ARROW'
        print("Objeto Empty 'Number_control' criado com sucesso na mesma posição do objeto selecionado!")

    obj = bpy.data.objects.get("Numbers")
    if obj is None:
        print("O objeto 'Numbers' não foi encontrado.")
    else:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        mask_modifier_zero = obj.modifiers.get("Mask_Zero")
        if mask_modifier_zero is None:
            print("O modificador 'Mask_Zero' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_zero = mask_modifier_zero.driver_add("show_viewport").driver
            var_zero = driver_zero.variables.new()
            var_zero.name = "var"
            var_zero.type = 'TRANSFORMS'
            target_zero = var_zero.targets[0]
            target_zero.id = bpy.data.objects.get("Number_control")
            if target_zero.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_zero.transform_type = 'LOC_Z'
                target_zero.transform_space = 'LOCAL_SPACE'
                driver_zero.expression = "0 <= var <= 0.99999999"

        mask_modifier_one = obj.modifiers.get("Mask_One")
        if mask_modifier_one is None:
            print("O modificador 'Mask_One' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_one = mask_modifier_one.driver_add("show_viewport").driver
            var_one = driver_one.variables.new()
            var_one.name = "var"
            var_one.type = 'TRANSFORMS'
            target_one = var_one.targets[0]
            target_one.id = bpy.data.objects.get("Number_control")
            if target_one.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_one.transform_type = 'LOC_Z'
                target_one.transform_space = 'LOCAL_SPACE'
                driver_one.expression = "1 <= var <= 1.99999999"

        mask_modifier_two = obj.modifiers.get("Mask_Two")
        if mask_modifier_two is None:
            print("O modificador 'Mask_Two' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_two = mask_modifier_two.driver_add("show_viewport").driver
            var_two = driver_two.variables.new()
            var_two.name = "var"
            var_two.type = 'TRANSFORMS'
            target_two = var_two.targets[0]
            target_two.id = bpy.data.objects.get("Number_control")
            if target_two.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_two.transform_type = 'LOC_Z'
                target_two.transform_space = 'LOCAL_SPACE'
                driver_two.expression = "2 <= var <= 2.99999999"

        mask_modifier_three = obj.modifiers.get("Mask_Three")
        if mask_modifier_three is None:
            print("O modificador 'Mask_Three' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_three = mask_modifier_three.driver_add("show_viewport").driver
            var_three = driver_three.variables.new()
            var_three.name = "var"
            var_three.type = 'TRANSFORMS'
            target_three = var_three.targets[0]
            target_three.id = bpy.data.objects.get("Number_control")
            if target_three.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_three.transform_type = 'LOC_Z'
                target_three.transform_space = 'LOCAL_SPACE'
                driver_three.expression = "3 <= var <= 3.99999999"

        mask_modifier_four = obj.modifiers.get("Mask_Four")
        if mask_modifier_four is None:
            print("O modificador 'Mask_Four' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_four = mask_modifier_four.driver_add("show_viewport").driver
            var_four = driver_four.variables.new()
            var_four.name = "var"
            var_four.type = 'TRANSFORMS'
            target_four = var_four.targets[0]
            target_four.id = bpy.data.objects.get("Number_control")
            if target_four.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_four.transform_type = 'LOC_Z'
                target_four.transform_space = 'LOCAL_SPACE'
                driver_four.expression = "4 <= var <= 4.99999999"

        mask_modifier_five = obj.modifiers.get("Mask_Five")
        if mask_modifier_five is None:
            print("O modificador 'Mask_Five' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_five = mask_modifier_five.driver_add("show_viewport").driver
            var_five = driver_five.variables.new()
            var_five.name = "var"
            var_five.type = 'TRANSFORMS'
            target_five = var_five.targets[0]
            target_five.id = bpy.data.objects.get("Number_control")
            if target_five.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_five.transform_type = 'LOC_Z'
                target_five.transform_space = 'LOCAL_SPACE'
                driver_five.expression = "5 <= var <= 5.99999999"

        mask_modifier_six = obj.modifiers.get("Mask_Six")
        if mask_modifier_six is None:
            print("O modificador 'Mask_Six' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_six = mask_modifier_six.driver_add("show_viewport").driver
            var_six = driver_six.variables.new()
            var_six.name = "var"
            var_six.type = 'TRANSFORMS'
            target_six = var_six.targets[0]
            target_six.id = bpy.data.objects.get("Number_control")
            if target_six.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_six.transform_type = 'LOC_Z'
                target_six.transform_space = 'LOCAL_SPACE'
                driver_six.expression = "6 <= var <= 6.99999999"

        mask_modifier_seven = obj.modifiers.get("Mask_Seven")
        if mask_modifier_seven is None:
            print("O modificador 'Mask_Seven' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_seven = mask_modifier_seven.driver_add("show_viewport").driver
            var_seven = driver_seven.variables.new()
            var_seven.name = "var"
            var_seven.type = 'TRANSFORMS'
            target_seven = var_seven.targets[0]
            target_seven.id = bpy.data.objects.get("Number_control")
            if target_seven.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_seven.transform_type = 'LOC_Z'
                target_seven.transform_space = 'LOCAL_SPACE'
                driver_seven.expression = "7 <= var <= 7.99999999"

        mask_modifier_eight = obj.modifiers.get("Mask_Eight")
        if mask_modifier_eight is None:
            print("O modificador 'Mask_Eight' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_eight = mask_modifier_eight.driver_add("show_viewport").driver
            var_eight = driver_eight.variables.new()
            var_eight.name = "var"
            var_eight.type = 'TRANSFORMS'
            target_eight = var_eight.targets[0]
            target_eight.id = bpy.data.objects.get("Number_control")
            if target_eight.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_eight.transform_type = 'LOC_Z'
                target_eight.transform_space = 'LOCAL_SPACE'
                driver_eight.expression = "8 <= var <= 8.99999999"

        mask_modifier_nine = obj.modifiers.get("Mask_Nine")
        if mask_modifier_nine is None:
            print("O modificador 'Mask_Nine' não foi encontrado no objeto 'Numbers'.")
        else:
            driver_nine = mask_modifier_nine.driver_add("show_viewport").driver
            var_nine = driver_nine.variables.new()
            var_nine.name = "var"
            var_nine.type = 'TRANSFORMS'
            target_nine = var_nine.targets[0]
            target_nine.id = bpy.data.objects.get("Number_control")
            if target_nine.id is None:
                print("O objeto 'Number_control' não foi encontrado.")
            else:
                target_nine.transform_type = 'LOC_Z'
                target_nine.transform_space = 'LOCAL_SPACE'
                driver_nine.expression = "9 <= var <= 9.99999999"

    print("Drivers adicionados com sucesso nos modificadores 'Mask_Zero' a 'Mask_Nine' do objeto 'Numbers'.")

    number_control = bpy.data.objects.get("Number_control")
    if number_control is None:
        print("O objeto 'Number_control' não foi encontrado.")
    else:
        transformation_constraint = number_control.constraints.new(type='TRANSFORM')
        print("Restrição de transformação adicionada ao objeto 'Number_control'.")

# Operador para executar o script "Make UX"
class UX_RIG_OT_make_ux(bpy.types.Operator):
    bl_idname = "ux_rig.make_ux"
    bl_label = "Make UX"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        make_ux()
        return {'FINISHED'}

# Painel para a aba "UX Rig"
class UX_RIG_PT_panel(bpy.types.Panel):
    bl_label = "UX Rig"
    bl_idname = "UX_RIG_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "UX Rig"

    def draw(self, context):
        layout = self.layout
        layout.operator("ux_rig.create_numbers")
        layout.operator("ux_rig.choose_font")
        layout.operator("ux_rig.make_ux")

# Registro das classes
def register():
    bpy.utils.register_class(UX_RIG_OT_create_numbers)
    bpy.utils.register_class(UX_RIG_OT_choose_font)
    bpy.utils.register_class(UX_RIG_OT_make_ux)
    bpy.utils.register_class(UX_RIG_PT_panel)

def unregister():
    bpy.utils.unregister_class(UX_RIG_OT_create_numbers)
    bpy.utils.unregister_class(UX_RIG_OT_choose_font)
    bpy.utils.unregister_class(UX_RIG_OT_make_ux)
    bpy.utils.unregister_class(UX_RIG_PT_panel)

if __name__ == "__main__":
    register()