# API规范

## 文档编号

SPEC-012

---

## 文档名称

统一API规范

---

# 一、角色构建

POST /characters/build

---

请求

{
"name":"Elon Musk",
"materials":[]
}

---

响应

{
"character_id":"xxx",
"status":"success"
}

---

# 二、查询角色

GET /characters/{id}

---

响应

{
"character_id":"",
"personality":{},
"knowledge":[]
}

---

# 三、角色聊天

POST /characters/chat

---

请求

{
"character_id":"xxx",
"message":"你为什么创业"
}

---

响应

{
"reply":"..."
}

---

# 四、更新角色

POST /characters/update

---

请求

{
"character_id":"xxx",
"new_material":[]
}

---

响应

{
"status":"success"
}

---

# 五、删除角色

DELETE /characters/{id}

---

响应

{
"status":"success"
}

---

# 六、统一响应格式

成功：

{
"success":true,
"data":{}
}

---

失败：

{
"success":false,
"error":"message"
}

---

# 七、版本管理

当前版本：

v1

所有接口前缀：

/api/v1/
