import pandas as pd
import os
import glob

def run_analysis():
    print("🚀 Starting Enhanced Data Processing...")
    
    # This version looks inside ALL subfolders recursively
    csv_files = glob.glob("**/*.csv", recursive=True)
    
    # Filter out the 'processed' file if it already exists to avoid double-counting
    csv_files = [f for f in csv_files if "processed_aadhaar_data" not in f]
    
    print(f"📂 Found {len(csv_files)} files across your folders.")

    if len(csv_files) == 0:
        print("❌ ERROR: No CSV files found! Check if they are in this folder or a subfolder.")
        return

    def aggregate_data(keyword):
        target_files = [f for f in csv_files if keyword.lower() in f.lower()]
        if not target_files:
            print(f"⚠️ No files found for: {keyword}")
            return pd.DataFrame()
        
        print(f"🔍 Processing {keyword} data from {len(target_files)} files...")
        dfs = []
        for f in target_files:
            try:
                temp_df = pd.read_csv(f)
                temp_df.columns = [c.strip().lower() for c in temp_df.columns]
                dfs.append(temp_df)
            except Exception as e:
                print(f"Could not read {f}: {e}")
        
        if not dfs: return pd.DataFrame()
        full_df = pd.concat(dfs, ignore_index=True)
        full_df['state'] = full_df['state'].astype(str).str.upper().str.strip()
        full_df['district'] = full_df['district'].astype(str).str.upper().str.strip()
        return full_df

    # 1. Process
    enrol = aggregate_data('enrolment')
    bio = aggregate_data('biometric')
    demo = aggregate_data('demographic')

    if enrol.empty:
        print("❌ ERROR: Enrolment data is missing. Analysis cannot continue.")
        return

    # 2. Merge
    print("📊 Merging datasets into a Master Record...")
    master = enrol.groupby(['state', 'district']).sum(numeric_only=True).reset_index()
    
    if not bio.empty:
        bio_grouped = bio.groupby(['state', 'district']).sum(numeric_only=True).reset_index()
        master = master.merge(bio_grouped, on=['state', 'district'], how='outer')
    
    if not demo.empty:
        demo_grouped = demo.groupby(['state', 'district']).sum(numeric_only=True).reset_index()
        master = master.merge(demo_grouped, on=['state', 'district'], how='outer')

    master.fillna(0, inplace=True)

    # 3. Winning Metrics
    master['total_enrol'] = master.get('age_0_5', 0) + master.get('age_5_17', 0) + master.get('age_18_greater', 0)
    master['total_updates'] = (master.get('bio_age_5_17', 0) + master.get('bio_age_17_', 0) + 
                              master.get('demo_age_5_17', 0) + master.get('demo_age_17_', 0))
    master['vulnerability_score'] = (master['total_updates'] / (master['total_enrol'] + 1))

    # 4. Save to the main folder
    output_name = 'processed_aadhaar_data.csv'
    master.to_csv(output_name, index=False)
    print(f"✅ SUCCESS: '{output_name}' created in your main folder!")

if __name__ == "__main__":
    run_analysis()
