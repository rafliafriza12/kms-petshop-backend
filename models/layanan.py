from db import db
from bson import ObjectId
from datetime import datetime
from models.kucing import get_kucing

COL = db.layanan
# layanan: {namaLayanan, deskripsi, benefit: [str], harga, diskon, durasiLayanan, kategori, status, createdAt, updatedAt}

def create_layanan(data):
    data["createdAt"] = data["updatedAt"] = datetime.utcnow()
    newLayanan = COL.insert_one(data)
    return COL.find_one({"_id": newLayanan.inserted_id})

def list_layanan(filters=None):
    return list(COL.find(filters or {}))

def get_layanan(id): return COL.find_one({"_id": ObjectId(id)})

def update_layanan(id, data):
    data["updatedAt"] = datetime.utcnow()
    COL.update_one({"_id": ObjectId(id)}, {"$set": data})
    return get_layanan(id)

def delete_layanan(id): COL.delete_one({"_id": ObjectId(id)})

def get_rekomendasi_layanan(id_kucing):
    kucing = get_kucing(id_kucing)
    if not kucing: 
        return []
    
    # Get all knowledge entries from database
    knowledge_col = db.knowledge
    knowledge_entries = list(knowledge_col.find({}))
    
    if not knowledge_entries:
        return []
    
    # Define weights for scoring
    WEIGHTS = {
        'kondisi_kesehatan': 0.35,
        'umur': 0.25,
        'berat': 0.20,
        'ras': 0.20
    }
    
    recommendations = []
    
    for knowledge in knowledge_entries:
        score = 0.0
        
        # 1. Check kondisi kesehatan (weight: 0.35)
        if 'kondisi' in knowledge and 'kondisiKesehatan' in kucing:
            kucing_kondisi = [k.lower() for k in (kucing.get('kondisiKesehatan', []) or [])]
            knowledge_kondisi = [k.lower() for k in (knowledge.get('kondisi', []) or [])]
            
            # Hitung jumlah kecocokan
            matches = sum(1 for kondisi in knowledge_kondisi if kondisi in kucing_kondisi)
            
            # Tambahkan skor sesuai jumlah match × bobot
            score += matches * WEIGHTS['kondisi_kesehatan']
        
        
        # 2. Check umur (weight: 0.25)
        kucing_umur = kucing.get('umur', 0)
        min_umur = knowledge.get('min_umur', 0)
        max_umur = knowledge.get('max_umur', float('inf'))
        
        if min_umur <= kucing_umur <= max_umur:
            score += WEIGHTS['umur']
        
        # 3. Check berat (weight: 0.20)
        kucing_berat = kucing.get('berat', 0)
        min_berat = knowledge.get('min_berat', 0)
        max_berat = knowledge.get('max_berat', float('inf'))
        
        if min_berat <= kucing_berat <= max_berat:
            score += WEIGHTS['berat']
        
        # 4. Check ras (weight: 0.20)
        if 'ras' in knowledge and 'ras' in kucing:
            kucing_ras = kucing.get('ras', '').lower()
            knowledge_ras = [r.lower() for r in (knowledge.get('ras', []) or [])]
            
            if kucing_ras in knowledge_ras:
                score += WEIGHTS['ras']
        
        # 5. Optional: Check tingkat aktivitas (bonus scoring)
        if 'tingkatAktivitas' in knowledge and 'tingkatAktivitas' in kucing:
            kucing_aktivitas = kucing.get('tingkatAktivitas', '').lower()
            knowledge_aktivitas = [a.lower() for a in (knowledge.get('tingkatAktivitas', []) or [])]
            
            if kucing_aktivitas in knowledge_aktivitas:
                # Small bonus for activity level match (not in main weights)
                score += 0.05
        
        # Only include recommendations with some score
        if score > 0:
            # Get the actual layanan data
            layanan = get_layanan(str(knowledge['layananId']))
            if layanan:
                recommendations.append({
                    'layanan': layanan,
                    'score': round(score, 2),
                    'knowledge_id': str(knowledge['_id'])
                })
    
    # Sort by score in descending order
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    return recommendations    
    
