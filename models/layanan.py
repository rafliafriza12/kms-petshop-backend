from db import db
from bson import ObjectId
from datetime import datetime
from models.kucing import get_kucing

COL = db.layanan
WEIGHTS = {
    'kondisi_kesehatan': 0.35,
    'umur': 0.25,
    'berat': 0.20,
    'ras': 0.10,
    'tingkat_aktivitas': 0.10
}
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
    """
    Get layanan recommendations for a specific kucing using rule-based scoring system.
    Returns recommendations sorted by compatibility score (0-1 scale).
    """
    try:
        # Validate input
        if not id_kucing:
            return []
        
        kucing = get_kucing(id_kucing)
        if not kucing: 
            return []
        
        knowledge_col = db.knowledge
        pipeline = [
            {
                "$lookup": {
                    "from": "layanan",
                    "localField": "layananId",
                    "foreignField": "_id",
                    "as": "layanan_info"
                }
            },
            {
                "$match": {
                    "layanan_info": {"$ne": []},
                    "layanan_info.status": {"$ne": "INACTIVE"}
                }
            }
        ]
        
        knowledge_entries = list(knowledge_col.aggregate(pipeline))
        
        if not knowledge_entries:
            return []
        
        recommendations = []
        
        for knowledge in knowledge_entries:
            try:
                total_score = 0.0
                
                # 1. Health conditions matching (35% weight)
                kondisi_score = _calculate_kondisi_score(kucing, knowledge)
                total_score += kondisi_score * WEIGHTS['kondisi_kesehatan']
                
                # 2. Age range matching (25% weight)
                umur_score = _calculate_umur_score(kucing, knowledge)                
                total_score += umur_score * WEIGHTS['umur']
                
                # 3. Weight range matching (20% weight)
                berat_score = _calculate_berat_score(kucing, knowledge)                
                total_score += berat_score * WEIGHTS['berat']
                
                # 4. Breed matching (10% weight)
                ras_score = _calculate_ras_score(kucing, knowledge)                
                total_score += ras_score * WEIGHTS['ras']
                
                # 5. Activity level matching (10% weight)
                aktivitas_score = _calculate_aktivitas_score(kucing, knowledge)                
                total_score += aktivitas_score * WEIGHTS['tingkat_aktivitas']
                
                # Only include recommendations with meaningful score (> 10% compatibility)
                if total_score >= 0.1:
                    layanan = knowledge['layanan_info'][0] if knowledge['layanan_info'] else None
                    
                    if layanan:
                        recommendations.append({
                            'layanan': layanan,
                            'score': round(total_score, 3),
                            'knowledge_id': str(knowledge['_id']),
                        })
            
            except Exception as e:
                print(f"Error processing knowledge entry {knowledge.get('_id', 'unknown')}: {str(e)}")
                continue
        
        # Sorting dan limit 10
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:10]
    
    except Exception as e:
        print(f"Error in get_rekomendasi_layanan: {str(e)}")
        return []

def _calculate_kondisi_score(kucing, knowledge):
    """Calculate health condition compatibility score (0-1 scale)"""
    try:
        if not knowledge.get('kondisi') or not kucing.get('kondisiKesehatan'):
            return 0.0
        
        kucing_kondisi = set(k.lower().strip() for k in kucing.get('kondisiKesehatan', []) if k)
        knowledge_kondisi = set(k.lower().strip() for k in knowledge.get('kondisi', []) if k)
        
        if not knowledge_kondisi:
            return 0.0
        
        # Calculate Jaccard similarity for better matching
        intersection = len(kucing_kondisi.intersection(knowledge_kondisi))
        union = len(kucing_kondisi.union(knowledge_kondisi))
        
        if union == 0:
            return 0.0
        
        return intersection / union
    except Exception:
        return 0.0

def _calculate_umur_score(kucing, knowledge):
    """Calculate age compatibility score (0-1 scale)"""
    try:
        kucing_umur = kucing.get('umur', 0)
        min_umur = knowledge.get('min_umur', 0)
        max_umur = knowledge.get('max_umur')
        
        if kucing_umur <= 0:
            return 0.0
        
        # Handle missing max_umur
        if max_umur is None or max_umur <= 0:
            max_umur = float('inf')
        
        # Exact range match gets full score
        if min_umur <= kucing_umur <= max_umur:
            return 1.0
        
        # Partial scoring for near misses (within 1 year tolerance)
        if kucing_umur < min_umur:
            diff = min_umur - kucing_umur
            return max(0.0, 1.0 - (diff / 2.0))  # Penalty decreases with distance
        elif kucing_umur > max_umur:
            diff = kucing_umur - max_umur
            return max(0.0, 1.0 - (diff / 2.0))  # Penalty decreases with distance
        
        return 0.0
    except Exception:
        return 0.0

def _calculate_berat_score(kucing, knowledge):
    """Calculate weight compatibility score (0-1 scale)"""
    try:
        kucing_berat = kucing.get('berat', 0)
        min_berat = knowledge.get('min_berat', 0)
        max_berat = knowledge.get('max_berat')
        
        if kucing_berat <= 0:
            return 0.0
        
        # Handle missing max_berat
        if max_berat is None or max_berat <= 0:
            max_berat = float('inf')
        
        # Exact range match gets full score
        if min_berat <= kucing_berat <= max_berat:
            return 1.0
        
        # Partial scoring for near misses (within 0.5kg tolerance)
        if kucing_berat < min_berat:
            diff = min_berat - kucing_berat
            return max(0.0, 1.0 - (diff / 1.0))  # 1kg tolerance
        elif kucing_berat > max_berat:
            diff = kucing_berat - max_berat
            return max(0.0, 1.0 - (diff / 1.0))  # 1kg tolerance
        
        return 0.0
    except Exception:
        return 0.0

def _calculate_ras_score(kucing, knowledge):
    """Calculate breed compatibility score (0-1 scale)"""
    try:
        if not knowledge.get('ras') or not kucing.get('ras'):
            return 0.0
        
        kucing_ras = kucing.get('ras', '').lower().strip()
        knowledge_ras = set(r.lower().strip() for r in knowledge.get('ras', []) if r)
        
        if not kucing_ras or not knowledge_ras:
            return 0.0
        
        # Exact match gets full score
        if kucing_ras in knowledge_ras:
            return 1.0
        
        # Partial matching for breed variations (e.g., "persian" vs "persia")
        for ras in knowledge_ras:
            if kucing_ras in ras or ras in kucing_ras:
                return 0.8  # Partial match
        
        return 0.0
    except Exception:
        return 0.0

def _calculate_aktivitas_score(kucing, knowledge):
    """Calculate activity level compatibility score (0-1 scale)"""
    try:
        if not knowledge.get('tingkatAktivitas') or not kucing.get('tingkatAktivitas'):
            return 0.0
        
        kucing_aktivitas = kucing.get('tingkatAktivitas', '').lower().strip()
        knowledge_aktivitas = set(a.lower().strip() for a in knowledge.get('tingkatAktivitas', []) if a)
        
        if not kucing_aktivitas or not knowledge_aktivitas:
            return 0.0
        
        if kucing_aktivitas in knowledge_aktivitas:
            return 1.0
        
        return 0.0
    except Exception:
        return 0.0    
    
