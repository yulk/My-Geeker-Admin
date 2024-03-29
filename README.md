## 前端启动

最新版官网：https://docs.spicyboy.cn/

我这的代码，是改了部分的（下面有前台文件的修改记录，只改了10来行），可以参考一下

```cmd
pnpm i
pnpm dev
```

## 后端启动

环境要求：python3 flask3
初始化环境
初始化数据库
启动

```shell
cd flask-backend
pip install -r requirements.txt
flask init_table
flask run
```
## admin 密码 12345678

## 功能

对接 GEEKER-ADMIN 的接口，做了登录、JWT、token、文件上传、文件下载 等接口
backend\flask_admin\apis\geeker_admin_api.py

但表的DB增删改也是直接用的json数据模拟，直接返回200,

因为需要完全模拟前台要求的结构没有太大价值，为了少动前台的代码，也不能我另外做一个数据库的结构来做，

尝试了一下，费时可能要1-2天放弃了。

所以没有做真实数据库的模拟CURD，请参考其他API，可以自己实现,比如：

backend\flask_admin\apis\user_api.py
flask-backend\flask_admin\apis\table_api.py

这里都有数据库CURD的真实操作

## 前台文件的修改记录

### code: 200 响应码表示成功
### msg 而不是 message

### 登录，密码设置

> Geeker-Admin\src\views\login\components\LoginForm.vue
去掉md5加密：
```js
      const { data } = await loginApi({ ...loginForm, password: loginForm.password });
```
返回：
{'code': 200, 'data': {'access_token': access_token}, 'msg': '登录成功'}

###  登录后不能访问菜单
> Geeker-Admin\src\api\modules\login.ts

```js
<!-- 登录后不能访问菜单 -->

// 获取菜单列表
export const getAuthMenuListApi = () => {
  // return http.get<Menu.MenuOptions[]>(PORT1 + `/menu/list`, {}, { loading: false });
  // 如果想让菜单变为本地数据，注释上一行代码，并引入本地 authMenuList.json 数据
  return authMenuList;
};

// 获取按钮权限
export const getAuthButtonListApi = () => {
  // return http.get<Login.ResAuthButtons>(PORT1 + `/auth/buttons`, {}, { loading: false });
  // 如果想让按钮权限变为本地数据，注释上一行代码，并引入本地 authButtonList.json 数据
  return authButtonList;
};
```

## 后端服务地址设置

> Geeker-Admin\src\api\config\servicePort.ts

```js
// 后端微服务模块前缀
export const PORT1 = "";
```

> Geeker-Admin\.env.development

```js
# 开发环境接口地址
VITE_API_URL = http://127.0.0.1:5000/api/v1

# 开发环境跨域代理，支持配置多个
# VITE_PROXY = [["/api/v1","http://127.0.0.1:5000/api/v1"]]
# VITE_PROXY = [["/api","https://www.fastmock.site/mock/f81e8333c1a9276214bcdbc170d9e0a0"]]
# VITE_PROXY = [["/api-easymock","https://mock.mengxuegu.com"],["/api-fastmock","https://www.fastmock.site"]]

```


> Geeker-Admin\vite.config.ts

```js
      // Load proxy configuration from .env.development
      // proxy: createProxy(viteEnv.VITE_PROXY) 注释掉这行
```

## stylelint 升级最新版报错，也去掉了。

 WARN  Issues with peer dependencies found
.
└─┬ stylelint-config-recommended-vue 1.5.0
  └─┬ stylelint-config-recommended 13.0.0
    └── ✕ unmet peer stylelint@^15.10.0: found 16.2.1

删除 Geeker-Admin\package.json 中 stylelint 依赖
    "stylelint": "^16.2.1",
    "stylelint-config-html": "^1.1.0",
    "stylelint-config-recess-order": "^5.0.0",
    "stylelint-config-recommended-scss": "^14.0.0",
    "stylelint-config-recommended-vue": "^1.5.0",
    "stylelint-config-standard": "^36.0.0",
    "stylelint-config-standard-scss": "^13.0.0",


## 目录

> flask-backend\flask_admin\__init__.py
> 这是主入口文件

> flask-backend\configs.py
> 配置文件

> flask-backend\flask_admin\orms
> sqlalchemy 模型

> flask-backend\flask_admin\schemas\__init__.py
> marshmallow schemas 用于序列化，反序列化

> flask-backend\flask_admin\apis\__init__.py
> flask-backend\flask_admin\apis\geeker_admin_api.py
> 后端API

## 后台修改记录

### 文件上传

### flask_reuploads 组件有个BUGS

> 当上传文件为全中文时，比如"图片.png", extension函数会返回空，

> 修改： D:\EMC2\python311\Lib\site-packages\flask_uploads\extensions.py
```python
def extension(filename: str) -> str:
    ext = os.path.splitext(filename)[1] if len(os.path.splitext(filename)[1]) >0 else os.path.splitext(filename)[0]
    if ext.startswith('.'):
        # os.path.splitext retains . separator
        ext = ext[1:]
    return ext
```

### 文件上传前端 views
Geeker-Admin\src\views\assembly\batchImport\index.vue
Geeker-Admin\src\views\assembly\uploadFile\index.vue

### 文件上传前端 components
Geeker-Admin\src\components\ImportExcel\index.vue
Geeker-Admin\src\components\Upload\Img.vue

### 文件上传前端 API
Geeker-Admin\src\api\modules\upload.ts

#### el-upload

```JS
        <el-upload
          action="#"
          class="upload"
          :drag="true"
          :limit="excelLimit"
          :multiple="true"
          :show-file-list="true"
          :http-request="uploadExcel"
          :before-upload="beforeExcelUpload"
          :on-exceed="handleExceed"
          :on-success="excelUploadSuccess"
          :on-error="excelUploadError"
          :accept="parameter.fileType!.join(',')"
        >

// 文件上传
const uploadExcel = async (param: UploadRequestOptions) => {
  let excelFormData = new FormData();
  excelFormData.append("file", param.file);
  excelFormData.append("isCover", isCover.value as unknown as Blob);
  await parameter.value.importApi!(excelFormData);
  parameter.value.getTableList && parameter.value.getTableList();
  dialogVisible.value = false;
};
```

### 文件上传后台配置

> backend\flask_admin\extensions\init_upload.py
>
```python
from flask import Flask
from flask_uploads import configure_uploads
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)
excels = UploadSet('excels', ('xls', 'xlsx'))
words = UploadSet('words', ('doc', 'docx'))


def init_upload(app: Flask):
    configure_uploads(app, photos)
    configure_uploads(app, excels)
    configure_uploads(app, words)
```

backend\configs.py
```python
class BaseConfig:
    UPLOADS_DEFAULT_DEST = 'upload'
    UPLOADED_PHOTOS_DEST = 'upload/photos'
    UPLOADED_EXCELS_DEST = 'upload/excels'
    UPLOADED_WORDS_DEST = 'upload/words'
```


### TODO: 用户信息表CURD
> 这块没做，下面为笔记记录
```js
  export interface ResUserList {
    id: string;
    username: string;
    gender: number;
    user: { detail: { age: number } };
    idCard: string;
    email: string;
    address: string;
    createTime: string;
    status: number;
    avatar: string;
    photo: any[];
    children?: ResUserList[];
  }

            {
                "id": "188809847655516924",
                "username": "吴秀兰",
                "gender": 1,
                "user": {
                    "detail": {
                        "age": 19
                    }
                },
                "idCard": "188809847655516924",
                "email": "j.qbonr@xskzhwtg.et",
                "address": "西藏自治区 日喀则地区",
                "createTime": "2009-03-27 20:15:30",
                "status": 0,
                "avatar": "https://i.imgtg.com/2023/01/16/QRa0s.jpg"
            }
```

> 可能要增加 department 表，存储部门信息，并在这 user 里面增加 departmentid 字段，进行关联，
```sql
CREATE TABLE `user` (
    `id` varchar(50) NOT NULL,
    `username` varchar(100) NOT NULL,
    `gender` tinyint NOT NULL,
    `user_detail_age` int NOT NULL,
    `idCard` varchar(50) NOT NULL,
    `email` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `createTime` datetime NOT NULL,
    `status` tinyint NOT NULL,
    `avatar` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 如果children字段也需要存储为子表形式
CREATE TABLE `user_children` (
    `parentId` varchar(50) NOT NULL,
    `childInfo` json NOT NULL,
    PRIMARY KEY (`parentId`),
    FOREIGN KEY (`parentId`) REFERENCES `user`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```

> 真实的项目做完再回来加强吧
