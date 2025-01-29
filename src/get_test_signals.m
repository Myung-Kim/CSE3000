% Parameters
fs_original = 96000; % Default sampling frequency used by generateStipaSignal
fs_resampled = 16000; % Target resampling frequency
test_lengths = [15]; % Lengths of test signals in seconds

% Generate, resample, and save multiple STIPA test signals
for i = 1:length(test_lengths)
    duration = test_lengths(i); % Current signal duration
    
    % Generate STIPA test signal at default frequency
    stipa_signal = generateStipaSignal(duration);
    fprintf('Generated STIPA signal of length %d samples at %d Hz for %d seconds.\n', ...
        length(stipa_signal), fs_original, duration);
    
    % Resample the signal to 16,000 Hz
    stipa_signal_resampled = resample(stipa_signal, fs_resampled, fs_original);
    fprintf('Resampled STIPA signal to %d Hz.\n', fs_resampled);
    
    % Save the resampled signal
    resampled_signal_path = sprintf('stipa_signal_%ds_16000Hz.wav', duration);
    audiowrite(resampled_signal_path, stipa_signal_resampled, fs_resampled);
    fprintf('Saved resampled STIPA signal at: %s\n', resampled_signal_path);
end
