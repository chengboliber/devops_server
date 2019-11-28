# -*- coding: utf-8 -*-


class AppError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '<%d %s>' % (self.code, self.message)


ErrArgs = AppError(1000, '参数错误')
ErrTokenFail = AppError(1001, '登录令牌失效')
ErrUserUnregistered = AppError(1002, '用户未注册')

ErrInternal = AppError(2000, '服务器内部错误')
ErrOperation = AppError(2001, '操作失败')
ErrInternalRequest = AppError(2002, '内部请求错误')

ErrPublishTaskNotFound = AppError(3000, '找不到发布任务')
ErrImmutablePblishTask = AppError(3001, '发布任务不可修改')
ErrTaskCantPublish = AppError(3002, '任务不可发布')
ErrTaskCantRollBack = AppError(3003, '任务不可回滚')
ErrAppRestartError = AppError(3004, '应用重启失败')
ErrCloneRepoError = AppError(3005, '拉取应用代码失败')
ErrCheckoutTagError = AppError(3006, '更新代码tag失败')
ErrTargetNoMatch = AppError(3007, '没有匹配的salt target')
ErrSaltCmdRetEmpty = AppError(3008, 'SALT执行结果返回为空')
ErrSameBinWithLastTime = AppError(3009, '编译后的执行码与上一版本相同')
# ErrServerID = AppError(3010, '服务器ID不是整数')
ErrBuildTaskNotFound = AppError(3011, '找不到编译任务')
ErrBuildCommandNotFound = AppError(3012, '找不到编译命令')
ErrAppNotBindServer = AppError(3013, '未绑定服务器')
ErrBuildFail = AppError(3014, '编译失败')
ErrPushBinary = AppError(3015, '推送执行文件到指定库失败')
ErrPathNotFound = AppError(3016, '找不到目录')
ErrCopyAppBinFail = AppError(3017, '拷贝执行码失败')
ErrAppStopError = AppError(3018, '应用停止失败')
ErrBakeAppBinFail = AppError(3019, '备份应用失败')
ErrExecHookFail = AppError(3020, '执行hook失败')
ErrQCloudUploadError = AppError(3021, '上传文件失败')
# ErrSaveFileInLocalError = AppError(3022, '文件存储到本地失败')
ErrRefreshCDNFail = AppError(3023, '刷新CDN失败')
# ErrMoveAppBinFail = AppError(3024, '移除执行码失败')
ErrAppRepeatedPubTagError = AppError(3025, '同一个应用不能有重复的发布tag')
ErrAppStartError = AppError(3026, '应用启动失败')
ErrAppRepeatedBuildTagError = AppError(3027, '此tag已经成功编译, 请勿重复提交')
ErrZipFileOnlyError = AppError(3028, '文件格式不对, 请使用zip格式')
ErrServerAlreadyDeploying = AppError(3029, '服务器已经进入部署状态')
ErrCDNCantRollback = AppError(3030, 'CDN应用不支持回滚')
ErrMkdirPath = AppError(3031, '创建目录失败')
ErrUpdateAppCfgFail = AppError(3032, '发布配置文件失败')
ErrImmutableBuildTask = AppError(3033, '编译任务不可修改')
ErrModifyBalancerWeight = AppError(3034, '修改负载均衡权重失败')
ErrUnauthorized = AppError(3035, '未授权操作')
ErrTagNotFound = AppError(3036, '在git上找不到tag')
ErrGitLocalChangesFound = AppError(3037, 'git检测到文件有变动, 无法切换分支')

ErrAppNotFound = AppError(4000, '找不到应用')
ErrServerNotFound = AppError(4001, '找不到服务器')
ErrAppServerNotFound = AppError(4002, '找不到应用-服务器关联')
ErrAppRepeatedError = AppError(4003, '应用名重复')
ErrAppBalancerInfoNotFound = AppError(4004, '找不到应用负载均衡信息')
ErrAppServerNotInSameEnv = AppError(4005, '不能绑定不同环境的应用与服务器')
ErrConfigConflicts = AppError(4006, '配置目录发生冲突')
