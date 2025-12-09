import numpy as np
import math

class Num_Cal:
    """Num_Cal 核心工具类：包含 fsolve、integral、ode45 功能"""
    def __init__(self, default_tol=1e-6, default_max_iter=100, default_max_depth=20):
        """
        初始化配置（统一默认参数，方便全局调整）
        参数：
            default_tol: 默认收敛容差（适用于所有功能）
            default_max_iter: 默认最大迭代次数（适用于 fsolve）
            default_max_depth: 默认最大递归深度（适用于 integral）
        """
        self.default_tol = default_tol
        self.default_max_iter = default_max_iter
        self.default_max_depth = default_max_depth

    # ---------------------- 通用辅助方法（内部使用，不对外暴露）----------------------
    def _num_deriv(self, fun, x, dim):
        """计算数值导数（单变量）或梯度（多变量）"""
        h = 1e-8
        if dim == 1:
            return (fun(x + h) - fun(x - h)) / (2 * h)
        else:
            grad = np.zeros_like(x)
            for i in range(dim):
                xh = x.copy()
                xh[i] += h
                xm = x.copy()
                xm[i] -= h
                grad[i] = (fun(xh) - fun(xm)) / (2 * h)
            return grad

    # ---------------------- 非线性方程求解（fsolve）----------------------
    def fsolve(self, fun, x0, tol=None, max_iter=None):
        """
        求解非线性方程 f(x)=0（单变量/多变量）
        参数：
            fun: 目标函数（输入 x，输出 f(x)）
            x0: 初始猜测值
            tol: 收敛容差（默认使用类的 default_tol）
            max_iter: 最大迭代次数（默认使用类的 default_max_iter）
        返回：
            x: 数值解, converged: 是否收敛, iter_num: 迭代次数
        """
        tol = tol if tol is not None else self.default_tol
        max_iter = max_iter if max_iter is not None else self.default_max_iter

        x = np.array(x0, dtype=np.float64)
        dim = x.size
        converged = False
        iter_num = 0

        # 单变量：牛顿-拉夫逊法
        if dim == 1:
            for i in range(max_iter):
                f_val = fun(x)
                if abs(f_val) < tol:
                    converged = True
                    break
                f_deriv = self._num_deriv(fun, x, dim)
                if abs(f_deriv) < 1e-12:
                    break
                x -= f_val / f_deriv
                iter_num = i + 1

        # 多变量：拟牛顿法（BFGS）
        else:
            H_inv = np.eye(dim)
            for i in range(max_iter):
                f_val = np.array(fun(x), dtype=np.float64).reshape(-1, 1)
                if np.linalg.norm(f_val) < tol:
                    converged = True
                    break
                grad = self._num_deriv(fun, x, dim).reshape(-1, 1)
                if np.linalg.norm(grad) < 1e-12:
                    break

                # 搜索方向
                d = -H_inv @ grad

                # Armijo 线搜索
                alpha = 1.0
                beta = 0.5
                c = 1e-4
                while np.linalg.norm(fun(x + alpha * d.flatten())) > np.linalg.norm(f_val) + c * alpha * (grad.T @ d):
                    alpha *= beta
                    if alpha < 1e-10:
                        break

                # 更新 x
                s = alpha * d
                x_new = x + s.flatten()

                # BFGS 更新 H_inv
                grad_new = self._num_deriv(fun, x_new, dim).reshape(-1, 1)
                y = grad_new - grad
                sT = s.T
                yT = y.T
                if yT @ s < 1e-12:
                    break  # 避免除以零
                I = np.eye(dim)
                term1 = (I - (s @ yT) / (yT @ s)) @ H_inv @ (I - (y @ sT) / (yT @ s))
                term2 = (s @ sT) / (yT @ s)
                H_inv = term1 + term2

                x = x_new
                iter_num = i + 1

        return x, converged, iter_num

    # ---------------------- 数值积分（integral）----------------------
    def integral(self, fun, a, b, tol=None, max_depth=None):
        """数值积分 ∫(a→b) fun(x) dx"""
        tol = tol if tol is not None else self.default_tol
        max_depth = max_depth if max_depth is not None else self.default_max_depth

        def _simpson(x0, x1, x2):
            """辛普森公式辅助函数"""
            h = (x2 - x0) / 2
            return h * (fun(x0) + 4 * fun(x1) + fun(x2)) / 3

        def _adaptive_simpson(a, b, fa, fb, fc, tol, depth):
            """递归自适应辛普森法"""
            mid = (a + b) / 2
            fmid = fun(mid)
            left = _simpson(a, (a+mid)/2, mid)
            right = _simpson(mid, (mid+b)/2, b)
            total = left + right
            err = abs(total - _simpson(a, mid, b)) / 15

            if depth >= max_depth:
                return total, err
            if err <= tol:
                return total, err
            else:
                left_val, left_err = _adaptive_simpson(a, mid, fa, fmid, (a+mid)/2, tol/2, depth+1)
                right_val, right_err = _adaptive_simpson(mid, b, fmid, fb, (mid+b)/2, tol/2, depth+1)
                return left_val + right_val, left_err + right_err

        fa = fun(a)
        fb = fun(b)
        fc = fun((a + b) / 2)
        val, err = _adaptive_simpson(a, b, fa, fb, fc, tol, depth=0)
        return val, err

    # ---------------------- 常微分方程求解（ode45）----------------------
    def ode45(self, fun, tspan, y0, tol=None, h0=1e-4, h_max=None):
        """求解 ODE：dy/dt = fun(t, y)"""
        tol = tol if tol is not None else self.default_tol
        t_start, t_end = tspan
        y0 = np.array(y0, dtype=np.float64).reshape(-1, 1)
        dim = y0.shape[0]

        # 初始化输出
        t = [t_start]
        y = [y0.flatten()]
        current_t = t_start
        current_y = y0
        h = h0
        h_max = h_max if h_max is not None else t_end - t_start

        # RK45 系数（固定公式）
        c = np.array([0, 1/5, 3/10, 4/5, 8/9, 1, 1])
        a = np.array([
            [0, 0, 0, 0, 0, 0],
            [1/5, 0, 0, 0, 0, 0],
            [3/40, 9/40, 0, 0, 0, 0],
            [44/45, -56/15, 32/9, 0, 0, 0],
            [19372/6561, -25360/2187, 64448/6561, -212/729, 0, 0],
            [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0],
            [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]
        ])
        b4 = np.array([16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55])
        b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0])

        while current_t < t_end:
            # 调整步长不超过 t_end
            if current_t + h > t_end:
                h = t_end - current_t

            # 计算 RK 中间值 k1~k6
            k = np.zeros((dim, 6))
            for i in range(6):
                t_i = current_t + c[i] * h
                y_i = current_y + h * np.sum(a[i, :i] * k[:, :i], axis=1).reshape(-1, 1)
                k[:, i] = fun(t_i, y_i.flatten())

            # 4阶和5阶解
            y4 = current_y + h * np.dot(k, b4).reshape(-1, 1)
            y5 = current_y + h * np.dot(k, b5[:-1]).reshape(-1, 1)

            # 误差估计与步长调整
            err = np.linalg.norm(y5 - y4, ord=np.inf)
            if err < tol:
                current_t += h
                current_y = y5
                t.append(current_t)
                y.append(current_y.flatten())
                h = min(h * (tol / (err + 1e-16))**0.2, h_max)
            else:
                h = h * (tol / (err + 1e-16))**0.2

            if h < 1e-12:
                raise RuntimeError("步长过小，可能无法收敛")

        return np.array(t), np.array(y)