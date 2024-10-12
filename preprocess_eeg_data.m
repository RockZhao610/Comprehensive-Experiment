function eegfinal_new = preprocess_eeg_data(eeg, true_frequencies)
    % 初始化参数
    numTargets = size(eeg, 1);
    numChannels = size(eeg, 2);
    numSamplingPoints = size(eeg, 3) - 73;  % 考虑到视觉延迟后的采样点数
    numTrials = size(eeg, 4);
    eegfinal = zeros(numTargets, numChannels, numSamplingPoints, numTrials);

    % 迭代每个目标频率
    for targetIdx = 1:numTargets
        % 提取并预处理每个目标的EEG数据
        eeg1 = squeeze(eeg(targetIdx, :, 74:end, :));  % 考虑采样同步以及视觉延迟
        eeg1 = permute(eeg1, [3, 1, 2]);  % 重组数据维度为 (trials, channels, time)

        % 去均值操作
        [trials, channels, time] = size(eeg1);
        eeg1_afterMean = zeros(size(eeg1));
        for trial = 1:trials
            for channel = 1:channels
                eeg1_afterMean(trial, channel, :) = eeg1(trial, channel, :) - mean(eeg1(trial, channel, :), 3);
            end
        end

        % 带通滤波器
        [b, a] = butter(2, [6, 15] / (256 / 2));  % 创建带通滤波器
        eeg1_afterButterFilter = zeros(size(eeg1_afterMean));
        for trial = 1:trials
            for channel = 1:channels
                eeg1_afterButterFilter(trial, channel, :) = filtfilt(b, a, squeeze(eeg1_afterMean(trial, channel, :)));
            end
        end

        % 陷波滤波器
        [m, n] = butter(2, [48, 52] / (256 / 2), 'stop');  % 创建陷波滤波器
        eeg1_afterNotchFilter = zeros(size(eeg1_afterButterFilter));
        for trial = 1:trials
            for channel = 1:channels
                eeg1_afterNotchFilter(trial, channel, :) = filtfilt(m, n, squeeze(eeg1_afterButterFilter(trial, channel, :)));
            end
        end

        % 存储处理后的数据
        eegfinal(targetIdx, :, :, :) = permute(eeg1_afterNotchFilter, [2, 3, 1]);  % 转置回正确的维度
    end

    % 创建新的数组并将频率存储在每个时间序列的开始
    eegfinal_new = zeros(numTargets, numChannels, numSamplingPoints + 1, numTrials);
    for i = 1:numTargets
        eegfinal_new(i, :, 1, :) = true_frequencies(i);  % 将频率存储在每个时间序列的开始
        eegfinal_new(i, :, 2:end, :) = eegfinal(i, :, :, :);  % 存储EEG数据
    end
end
