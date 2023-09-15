// // const promise = new Promise((resolve, reject) => {
// //   // �첽����
// //   setTimeout(() => {
// //     if (Math.random() < 0.5) {
// //       resolve('success');
// //     } else {
// //       reject('error');
// //     }
// //   }, 1000);
// // });
// //
// // promise.then(result => {
// //   console.log(result);
// // }).catch(error => {
// //   console.log(error);
// // });
//
// // new Promise(function (resolve, reject) {
// //     var a = 0;
// //     var b = 0;
// //     if (b == 0) reject("Divide zero");
// //     else resolve(a / b);
// // }).then(function (value) {
// //     console.log("a / b = " + value);
// // }).catch(function (err) {
// //     console.log(err);
// // }).finally(function () {
// //     console.log("End");
// // });
//
// // new Promise(function (resolve, reject) {
// //     console.log(1111);
// //     var xz = 0;
// //     if (xz == 0){  // resolve(),reject()���������������򣬽������ڸ÷���(��ʼ����)����Ч
// //         resolve(2222);
// //     }
// //     else{
// //         reject("xz != 0");
// //     }
// // }).then(function (value) {
// //     console.log(value);
// //     // throw "An error xz";
// //     return 3333;
// // }).then(function (value) {
// //     console.log(value);
// //     // reject("xz != 0"); // �����򲻴��ڣ�defined
// //     throw "An error";  // throw �ܳ��쳣
// // }).catch(function (err) {  // �����쳣
// //     console.log(err);  // ��ӡ�ַ���
// // });
//
// var promise =new Promise(function(resolve,reject){
//     //To Do Ҫ�첽ִ�е����飬����첽ִ�е������п��ܳɹ�ִ����ϣ���ôPromise����fulfilled״̬�����ִ��ʧ������rejected;
//     //������Դ��룬��Ϊ����Ϊrejected״̬;
//     console.log("����ǰ������Promise�����״̬��pending�������У�����Ϊrejected���Ѿܾ���");
//     reject("����ǰ������Promise�����״̬��pending�������У�����Ϊrejected���Ѿܾ���"); //��Ȼ�˴�Ҳ��������Ϊfulfilled(�����)״̬
// })
//
// promise.then(//���õ�һ��then()
//     success=>{
//         console.log("�첽ִ�гɹ���״̬Ϊ��fulfilled���ɹ��󷵻صĽ���ǣ�"+success);
//         return(" ��ǰ success ");
//     },
//     error=>{
//         console.log("�첽ִ��ʧ�ܣ�״̬Ϊrejected��ʧ�ܺ󷵻صĽ���ǣ�"+error);
//         return(" ��ǰ error ");
//     }
// ).then(
//     //���õڶ���then() ��Ϊ���õ�һ��then()�������ص���һ���µ�promise���󣬴˶����״̬�������success����error�����ص�������ִ����������ģ�
//     //����ص�����������ִ����ϣ����µ�promise�����״̬Ϊfulfilled������ִ��success2,����ص������޷�����ִ�У���promise״̬Ϊrejected;����ִ��error2
//     success2=>{
//         console.log("��һ��then�Ļص�����ִ�гɹ� �ɹ����ؽ����"+success2);
//         throw(" ��ǰ success2 ");//�Զ����쳣�׳�
//     },
//     error2=>{
//         console.log("��һ��then�Ļص�����ִ��ʧ�� ʧ�ܷ��ؽ����"+error2);
//         return(" ��ǰ error2 ");
//     }
// ).catch(err=>{
//     //��success2����error2ִ�б���ʱ��catch�Ჶ���쳣;
//     console.log("�����쳣��"+err);
// });

// var promise = new Promise(function(resolve,reject){
//     //To Do 要异步执行的事情，这个异步执行的事情有可能成功执行完毕，那么Promise将是fulfilled状态，如果执行失败则是rejected;
//     //下面测试代码，人为设置为rejected状态;
//     reject("将当前构建的Promise对象的状态由pending（进行中）设置为rejected（已拒绝）"); //当然此处也可以设置为fulfilled(已完成)状态
// })
//
// promise.then(//调用第一个then()
//     success=>{
//         console.log("异步执行成功，状态为：fulfilled，成功后返回的结果是："+success);
//         return(" 当前 success ");
//     },
//     error=>{
//         console.log("异步执行失败，状态为rejected，失败后返回的结果是："+error);
//         throw(" 当前 error1 ");
//         return(" 当前 error ");
//     }
// ).then(
//     //调用第二个then() 因为调用第一个then()方法返回的是一个新的promise对象，此对象的状态由上面的success或者error两个回调函数的执行情况决定的：
//     //如果回调函数能正常执行完毕，则新的promise对象的状态为fulfilled，下面执行success2,如果回调函数无法正常执行，则promise状态为rejected;下面执行error2
//     success2=>{
//         console.log("第一个then的回调函数执行成功 成功返回结果："+success2);
//         throw(" 当前 success2 ");//自定义异常抛出
//     },
//     error2=>{
//         console.log("第一个then的回调函数执行失败 失败返回结果："+error2);
//         throw(" 当前 error2 ");
//         return(" 当前 error2 ");
//     }
// ).catch(err=>{
//     //当success2或者error2执行报错时，catch会捕获异常;
//     console.log("捕获异常："+err);
// });

function sleep(ms){
    return new Promise(function(resolve, reject){
        setTimeout(reject, ms)
    })
}
sleep(1000).then(
    success_xz=>{
        console.log("finished")
    },
    error_xz=>{
        console.log("failed")
    }
);

console.log("小洲");
"异步是个什么东西呢？异步就相当于我在执行一条任务，" +
"而这条任务呢，我不知道他什么时候做完，但是我又不想让他卡住我整个的线程，" +
"但是当他做完的时候呢，我们又必须要知道任务是否已经完成了，如果他失败的时候，我们也必须知道任务是否已经失败了。"

// 1、在创建promise对象时，需要传入自己要执行的方法(myExecutorFunction)；
// 2、在myExecutorFunction执行完之后，会进入then事件的方法中；
// 3、then事件可以后边嵌套，但是myExecutorFunction只会执行一次，之后会进入嵌套的then事件中；
// 4、逆向的目的是找到创建promise对象时传入的myExecutorFunction，myExecutorFunction很大可能是加密方法；

// apply() 解释， o.apply(this, arguments) == this.o(arguments), arguments是一个数组，里面存储了未知个参数
//               r.apply(e, t) == e.r(t), 给e对象添加了一个方法并传入了参数t，并且会调用(执行)该方法

// 平坦流 switch case入口，可动态修改下一个case的进入条件；
// 平坦流分析方法，出现特征(wrap、u.prev = u.next)
// 先跟头，找return的地方并且没有u.next，定位断点之后根据case的进入条件找上一个case方法；


/* 平坦流 分解顺序结构方式
* 1、出现特征(wrap、u.prev = u.next)
* 2、先找尾部，找带有return的case并且没有u.next，或存在sent，下断后根据case的进入条件找上一个case方法；
* 3、u.sent 解释
* case 0:
* u.next = 8;
* return a.apply(this, o);
* 解释 case 8: f = u.sent，u.sent == case 0:的返回值return a.apply(this, o);
* 最后 f = a.apply(this, o);
*
* 4、可以删除部分代码
* 4.1、break可以删除
* 4.2、当前case 0，假如下一个case中 存在 u.sent 则可以将当前case 0的return进行删除
*
* 5、 特征 while(e.length)  .then(.shift()), .shit() == pop() 取出第0个元素，并删除
* */