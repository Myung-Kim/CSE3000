% Paths
degraded_base_folder = 'clean_stipa_zero'; % Base folder containing subfolders for degraded files
output_folder_name = 'stipa_scores_zero'; % Name of the folder to save the .csv file
output_folder_path = fullfile(pwd, output_folder_name);

% Ensure the output folder exists
if ~exist(output_folder_path, 'dir')
    mkdir(output_folder_path);
end

% List all T60 folders
t60_folders = dir(degraded_base_folder);
t60_folders = t60_folders([t60_folders.isdir] & ~ismember({t60_folders.name}, {'.', '..'})); % Exclude '.' and '..'

% Helper function to calculate STIPA score for a single RIR folder
function process_rir_folder_without_reference(rir_folder_path, output_csv_path, rir_subfolder_name)
    % Open the CSV file in append mode
    fid = fopen(output_csv_path, 'a');

    % List all degraded files
    degraded_files = dir(fullfile(rir_folder_path, '*.wav'));

    % Process each degraded file
    for i = 1:numel(degraded_files)
        degraded_file_path = fullfile(rir_folder_path, degraded_files(i).name);

        try
            % Read degraded audio file
            [degraded_signal, fs_degraded] = audioread(degraded_file_path);

            % Calculate STIPA score without using a reference signal
            stipa_score = stipa(degraded_signal, fs_degraded);

            % Add the subfolder name to the degraded file name
            file_record_name = sprintf('%s/%s', rir_subfolder_name, degraded_files(i).name);

            % Write the score to the CSV file
            fprintf(fid, '%s,%.3f\n', file_record_name, stipa_score);
            fprintf('Processed %s: STIPA=%.3f\n', file_record_name, stipa_score);
        catch ME
            % Handle errors and log them
            fprintf(fid, '%s,Error: %s\n', degraded_files(i).name, ME.message);
            fprintf('Failed to process %s: %s\n', degraded_files(i).name, ME.message);
        end
    end

    fclose(fid);
end

% Process each T60 folder
for t = 1:numel(t60_folders)
    t60_folder = t60_folders(t).name;
    t60_folder_path = fullfile(degraded_base_folder, t60_folder);
    output_csv_path = fullfile(output_folder_path, sprintf('%s_stipa_scores.csv', t60_folder));

    % List all RIR folders within the T60 folder
    rir_folders = dir(t60_folder_path);
    rir_folders = rir_folders([rir_folders.isdir] & ~ismember({rir_folders.name}, {'.', '..'})); % Exclude '.' and '..'

    % Process each RIR folder
    for r = 1:numel(rir_folders)
        rir_folder = rir_folders(r).name;
        rir_folder_path = fullfile(t60_folder_path, rir_folder);

        % Append results to the corresponding CSV file
        process_rir_folder_without_reference(rir_folder_path, output_csv_path, rir_folder);
    end
end

fprintf('All STIPA scores saved in %s\n', output_folder_path);
