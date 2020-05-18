# CTFd-Fox

此插件为了解决静态flag能够直接在以太坊区块链上查看的问题，仅需在合约代码中添加一个验证函数。

[example.sol](github.com/publicqi/CTFd-Fox/blob/master/example.sol)

---

### 安装

1. 将repo下载到 `plugins` 目录
2. `pip install web3`
3. 在 `address_flag/web3utils.py`中设置HTTPProvider，推荐使用**Infura**，请确认使用的节点（大多数情况是Ropsten）

---

### 如何创建题目

1. 创建 **smart contract** 类型的challenge且不需要设置flag
2. 进入到此题的设置页面，添加类型为**address**的flag
3. 填入合约地址

---

### flag的验证机制以及如何提交flag？

需要出题人在合约代码中创建**leaveMsg()**函数

[example.sol](github.com/publicqi/CTFd-Fox/blob/master/example.sol)

此函数与getFlag()相似：如果某些条件达成了, sender可以用此函数留下message。用户需要提交此次调用函数的**transaction hash **。 [web3utils.py](github.com/publicqi/CTFd-Fox/blob/master/address_flag/web3utils.py) 会检查 **transaction 是否成功**以及 **message是否匹配用户的邮箱**

也就是说，在用户完成了一些要求后（比如转走合约所有的钱），用户需要调用leaveMsg函数留下自己的邮箱，并且提交此次调用的transaction hash。

---

### 自定义leaveMsg函数

在[web3utils.py](github.com/publicqi/CTFd-Fox/blob/master/address_flag/web3utils.py)中，代码会确认此transaction hash调用的函数与leaveMsg函数匹配，但你可以修改`func_header`。

---

### TODO

- 使用uuid
- Challenge specific func_header