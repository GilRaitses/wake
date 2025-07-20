# 🔥 Firestore Setup Instructions

## Required: Enable Firestore API & Configure Authentication

### Step 1: Enable Firestore API in Google Cloud Console

1. **Direct Link (Fastest):**
   ```
   https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=orca-466204
   ```

2. **Manual Navigation:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select project **`orca-466204`**
   - Navigate: **APIs & Services** → **Library**
   - Search: **"Cloud Firestore API"**
   - Click **ENABLE**

### Step 2: Create Firestore Database

1. Go to **Firestore** in left sidebar
2. Click **"Create database"**
3. **Mode**: Choose **Production mode** (recommended)
4. **Location**: Select **`us-west1`** (closest to your region)
5. Click **"Create"**

### Step 3: Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"CREATE SERVICE ACCOUNT"**
3. **Details:**
   - **Name:** `orcast-firestore-admin`
   - **Description:** `ORCAST Firestore database access`
4. Click **"CREATE AND CONTINUE"**
5. **Roles:** Add these roles:
   - **Cloud Datastore User**
   - **Firebase Admin SDK Administrator Service Agent**
6. Click **"CONTINUE"** → **"DONE"**

### Step 4: Download Service Account Key

1. Click on your **`orcast-firestore-admin`** service account
2. Go to **"Keys"** tab  
3. Click **"ADD KEY"** → **"Create new key"**
4. Choose **JSON** format
5. **Download** and **save as:**
   ```
   /Users/gilraitses/PNW_summer25/firebase_orca_app/config/serviceAccountKey.json
   ```

### Step 5: Verify Setup

Run the verification script to confirm everything is working:

```bash
cd /Users/gilraitses/PNW_summer25/firebase_orca_app
node verify-integration.js
```

**Expected output:**
```
✅ Firestore Connection: PASS
✅ Data Sources: PASS  
✅ Map Access: PASS
🎯 Overall: 5/5 checks passed
🎉 INTEGRATION VERIFIED: Whale data is accessible to map configuration objects!
```

## Security Notes

- ✅ **Service account key** added to `.gitignore`
- ✅ **No fallback modes** - requires proper setup
- ✅ **Production-ready** configuration

## Troubleshooting

### Error: "Service account key not found"
- **Solution:** Download key from Google Cloud Console and place in `config/serviceAccountKey.json`

### Error: "PERMISSION_DENIED: Cloud Firestore API has not been used"
- **Solution:** Enable Firestore API following Step 1 above

### Error: "Firestore not initialized"
- **Solution:** Complete all setup steps above, especially service account creation

## Collections Created

Once setup is complete, these Firestore collections will be created:

- **`whale_sightings`** - Individual whale sighting records
- **`import_status`** - Data import tracking and status
- **`map_data_cache`** - Pre-computed map hotspots and bounds

## API Access

Your map feature can access data via:

```javascript
// REST API
GET /api/map-sightings
GET /api/firestore-status

// Direct Firestore (when authenticated)
db.collection('whale_sightings').where('mapReady', '==', true)
```

## Next Steps

1. ✅ Complete Firestore setup above
2. ✅ Run verification script  
3. ✅ Test API endpoints
4. 🚀 Build your map feature using live whale data! 