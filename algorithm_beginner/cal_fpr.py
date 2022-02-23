# 指标计算示例函数

def cal_pn(gate, label_predict, label_true):
    predict_pass = np.greater(label_predict, gate)
    tp = np.sum(np.logical_and(predict_pass, label_true))
    fp = np.sum(np.logical_and(predict_pass, np.logical_not(label_true)))
    tn = np.sum(np.logical_and(np.logical_not(predict_pass), np.logical_not(label_true)))
    fn = np.sum(np.logical_and(np.logical_not(predict_pass), label_true))
    return tp,fp,tn,fn

def TPR_FPR( label_predict, label_true, fpr_target = 0.001):
    # acer_min = 1.0
    # thres_min = 0.0
    # re = []

    # FPR:  Fake Positive Rate 假阳率
    # FPR = FP / (FP + TN)

    # TPR: True Positive Rate 真阳率
    # TPR = TP / (TP + FN)

    thresholds = np.arange(0.0, 1.0, 0.0002)
    nrof_thresholds = len(thresholds)

    fpr = np.zeros(nrof_thresholds)
    FPR = 0.0
    for threshold_idx, threshold in enumerate(thresholds):
        if threshold < 1.0:
            tp, fp, tn, fn = cal_pn(threshold, label_predict, label_true)
            #print("tp, fp, tn, fn = %d, %d, %d, %d"%(tp, fp, tn, fn))
            FPR = fp / (fp*1.0 + tn*1.0)
            TPR = tp / (tp*1.0 + fn*1.0)
        fpr[threshold_idx] = FPR
        if threshold_idx%100==0:
            print("gate %.3f: FPR=%.4f, TPR=%.4f"%(threshold, FPR, TPR))

    if np.max(fpr) >= fpr_target:
        f = interpolate.interp1d(np.asarray(fpr), thresholds, kind= 'slinear')
        threshold = f(fpr_target)
    else:
        threshold = 0.0

    tp, fp, tn, fn = cal_pn(threshold, label_predict, label_true)
    print("threshold=%.3f: tp, fp, tn, fn = %d, %d, %d, %d"%(threshold, tp, fp, tn, fn))
    FPR = fp / (fp * 1.0 + tn * 1.0)
    TPR = tp / (tp * 1.0 + fn * 1.0)

    #print(str(FPR)+' '+str(TPR))
    return FPR,TPR

# 使用原始验证集数据的评估函数, 这里data为预处理好的数据
def evaluate_tpr_original(model, data, label, fpr_target):
    start = time.process_time()
    label_p=model_predict(model, data, label)  #输出为真脸的概率
    print("use %f s"%(time.process_time()-start))
    label_true=label
    label_predict=label_p
    FPR,TPR = TPR_FPR( label_predict, label_true, fpr_target )
    print("%.4f TPR@FPR=%.4f"%(TPR,FPR))