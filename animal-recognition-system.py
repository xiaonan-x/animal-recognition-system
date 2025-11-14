import tkinter as tk
from tkinter import ttk, scrolledtext

# 1. 定义产生式规则库（严格对应PPT中r1-r15）
rules = [
    # r1-r8：中间结论（哺乳动物、鸟、食肉动物、有蹄类）
    {"id": "r1", "conditions": ["有毛发"], "conclusion": "哺乳动物"},
    {"id": "r2", "conditions": ["有奶"], "conclusion": "哺乳动物"},
    {"id": "r3", "conditions": ["有羽毛"], "conclusion": "鸟"},
    {"id": "r4", "conditions": ["会飞", "会下蛋"], "conclusion": "鸟"},
    {"id": "r5", "conditions": ["吃肉"], "conclusion": "食肉动物"},
    {"id": "r6", "conditions": ["有犬齿", "有爪", "眼盯前方"], "conclusion": "食肉动物"},
    {"id": "r7", "conditions": ["哺乳动物", "有蹄"], "conclusion": "有蹄类动物"},
    {"id": "r8", "conditions": ["哺乳动物", "反刍动物"], "conclusion": "有蹄类动物"},
    # r9-r15：最终动物结论
    {"id": "r9", "conditions": ["哺乳动物", "食肉动物", "黄褐色", "身上有暗斑点"], "conclusion": "金钱豹"},
    {"id": "r10", "conditions": ["哺乳动物", "食肉动物", "黄褐色", "身上有黑色条纹"], "conclusion": "虎"},
    {"id": "r11", "conditions": ["有蹄类动物", "长脖子", "长腿", "身上有暗斑点"], "conclusion": "长颈鹿"},
    {"id": "r12", "conditions": ["有蹄类动物", "身上有黑色条纹"], "conclusion": "斑马"},
    {"id": "r13", "conditions": ["鸟", "长脖子", "长腿", "不会飞", "有黑白二色"], "conclusion": "鸵鸟"},
    {"id": "r14", "conditions": ["鸟", "会游泳", "不会飞", "有黑白二色"], "conclusion": "企鹅"},
    {"id": "r15", "conditions": ["鸟", "善飞"], "conclusion": "信天翁"}
]

# 2. 推理核心函数
def infer_animal(selected_features):
    """
    根据选择的特征推理动物
    :param selected_features: 列表，用户选择的初始特征
    :return: 元组（推理过程日志，最终动物结果）
    """
    # 初始化综合数据库（初始特征 + 推理出的中间结论）
    fact_base = set(selected_features)
    log = []
    log.append(f"初始选择特征：{', '.join(selected_features)}\n")
    
    # 循环匹配规则，直到无新结论可添加
    while True:
        new_conclusion = None
        matched_rule = None
        
        # 遍历所有规则，检查前提是否完全满足且结论未在数据库中
        for rule in rules:
            rule_conditions = set(rule["conditions"])
            # 前提全部在事实库中，且结论不在事实库中
            if rule_conditions.issubset(fact_base) and rule["conclusion"] not in fact_base:
                new_conclusion = rule["conclusion"]
                matched_rule = rule
                break  # 每次匹配一条规则（按规则顺序优先）
        
        # 无新结论时退出循环
        if not new_conclusion:
            log.append("已无匹配规则，推理结束\n")
            break
        
        # 添加新结论到事实库，并记录日志
        fact_base.add(new_conclusion)
        log.append(f"匹配规则【{matched_rule['id']}】：IF {', '.join(matched_rule['conditions'])} THEN {new_conclusion}")
        log.append(f"当前综合数据库：{', '.join(sorted(fact_base))}\n")
    
    # 提取最终动物结果（排除中间结论：哺乳动物、鸟、食肉动物、有蹄类动物）
    intermediate_conclusions = {"哺乳动物", "鸟", "食肉动物", "有蹄类动物"}
    animal_results = [fact for fact in fact_base if fact not in intermediate_conclusions and fact not in selected_features]
    
    if animal_results:
        return ("\n".join(log), f"推理结果：{animal_results[0]}")  # 仅支持单动物识别
    else:
        return ("\n".join(log), "推理结果：未匹配到任何已知动物，请检查特征选择")

# 3. Tkinter GUI界面实现
class AnimalRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("动物产生式识别系统")
        self.root.geometry("800x600")  # 窗口大小
        self.selected_features = []  # 存储用户选择的特征
        
        # 3.1 特征选择区域（左侧）
        self.feature_frame = ttk.LabelFrame(root, text="选择动物特征")
        self.feature_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsw")
        
        # 所有可能的特征（从规则库提取，覆盖所有前提）
        all_features = [
            "有毛发", "有奶", "有羽毛", "会飞", "会下蛋", "吃肉",
            "有犬齿", "有爪", "眼盯前方", "有蹄", "反刍动物",
            "黄褐色", "身上有暗斑点", "身上有黑色条纹", "长脖子",
            "长腿", "不会飞", "会游泳", "有黑白二色", "善飞"
        ]
        
        # 创建特征选择复选框
        self.feature_vars = {}
        for idx, feature in enumerate(all_features):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(
                self.feature_frame, text=feature, variable=var,
                command=lambda f=feature, v=var: self.update_selected(f, v)
            )
            chk.grid(row=idx//2, column=idx%2, padx=5, pady=3, sticky="w")
            self.feature_vars[feature] = var
        
        # 3.2 操作与结果显示区域（右侧）
        self.result_frame = ttk.LabelFrame(root, text="推理与结果")
        self.result_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # 运行推理按钮
        self.run_btn = ttk.Button(
            self.result_frame, text="开始推理", command=self.run_inference
        )
        self.run_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # 重置按钮
        self.reset_btn = ttk.Button(
            self.result_frame, text="重置选择", command=self.reset_selection
        )
        self.reset_btn.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # 推理过程日志显示（滚动文本框）
        self.log_text = scrolledtext.ScrolledText(
            self.result_frame, width=60, height=15, font=("Arial", 10)
        )
        self.log_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        # 最终结果显示（标签）
        self.result_label = ttk.Label(
            self.result_frame, text="", font=("Arial", 12, "bold"), foreground="red"
        )
        self.result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")
    
    # 更新用户选择的特征
    def update_selected(self, feature, var):
        if var.get():
            self.selected_features.append(feature)
        else:
            self.selected_features.remove(feature)
    
    # 执行推理并更新界面
    def run_inference(self):
        if not self.selected_features:
            self.log_text.delete(1.0, tk.END)
            self.result_label.config(text="请先选择至少一个动物特征！")
            return
        
        # 调用推理函数
        inference_log, result = infer_animal(self.selected_features)
        
        # 更新界面显示
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(1.0, inference_log)
        self.result_label.config(text=result)
    
    # 重置所有选择
    def reset_selection(self):
        self.selected_features.clear()
        for var in self.feature_vars.values():
            var.set(False)
        self.log_text.delete(1.0, tk.END)
        self.result_label.config(text="")

# 4. 程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalRecognitionGUI(root)
    # 窗口布局自适应
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    app.result_frame.grid_rowconfigure(1, weight=1)
    root.mainloop()