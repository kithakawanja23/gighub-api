from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

app = FastAPI(
    title="GigHub Nairobi Freelance Gigs API",
    description="Backend API system for managing freelance job listings in Nairobi. Student Reg: C027-01-0834/2024",
    version="1.0.0"
)

# Assigned Configuration Based on Reg No: C027-01-0834/2024
# Categories: "Development", "Design", "Writing"
# Currency: KES
# Total Initial Gigs: 9

GIG_CATEGORIES = Literal["Development", "Design", "Writing"]
GIG_STATUSES = Literal["Open", "In Progress", "Closed"]

# --- Part 4: Pydantic Models ---

class GigCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="The job title")
    description: str = Field(..., min_length=20, max_length=500, description="Detailed job description")
    category: GIG_CATEGORIES = Field(..., description="Must be Development, Design, or Writing")
    budget: float = Field(..., gt=0, description="Budget must be greater than 0")
    client_name: str = Field(..., min_length=2, max_length=50, description="Client publishing the gig")

class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0, description="Updated budget must be greater than 0")
    status: Optional[GIG_STATUSES] = Field(None, description="Must be Open, In Progress, or Closed")


# --- Part 2: Initial Dataset (9 Gigs) ---

gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a responsive React dashboard for an eCommerce fintech startup based in Westlands.",
        "category": "Development",
        "budget": 45000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Mobile App UI/UX Design",
        "description": "Design sleek high-fidelity Figma prototypes for a ride-hailing mobile application system.",
        "category": "Design",
        "budget": 30000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Omwamba"
    },
    {
        "id": 3,
        "title": "Technical Blog Post Writing",
        "description": "Write five high-quality, SEO-optimized technical articles explaining cloud computing metrics.",
        "category": "Writing",
        "budget": 12000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Alice Wakio"
    },
    {
        "id": 4,
        "title": "FastAPI Backend Integration",
        "description": "Build scalable REST endpoints using FastAPI framework and connect them with PostgreSQL backend.",
        "category": "Development",
        "budget": 60000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Kamau"
    },
    {
        "id": 5,
        "title": "Company Profile Logo Suite",
        "description": "Create modern professional typography logos and complete brand identity guidelines.",
        "category": "Design",
        "budget": 15000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Mercy Chepkoech"
    },
    {
        "id": 6,
        "title": "Academic Research Editing",
        "description": "Review, edit, and crosscheck citations for an internal economic business thesis write-up.",
        "category": "Writing",
        "budget": 18000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "John Kiprop"
    },
    {
        "id": 7,
        "title": "E-Commerce Website Setup",
        "description": "Deploy a custom tailored WooCommerce online store integrated local payment gateways.",
        "category": "Development",
        "budget": 35000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Sarah Hassan"
    },
    {
        "id": 8,
        "title": "Social Media Banner Assets",
        "description": "Design 15 digital marketing banner assets for ongoing Instagram and LinkedIn campaigns.",
        "category": "Design",
        "budget": 8500.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Evans Mwangi"
    },
    {
        "id": 9,
        "title": "Copywriting for Landing Page",
        "description": "Write persuasive, conversion-focused sales copies for a SaaS landing product page launch.",
        "category": "Writing",
        "budget": 10000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Grace Atieno"
    }
]


# --- Part 3: API Endpoints ---

# 1. List all available gigs (with optional filtering by category and budget ranges)
@app.get("/gigs")
def get_gigs(
    category: Optional[str] = Query(None, description="Filter gigs by category"),
    min_budget: Optional[float] = Query(None, description="Minimum budget limit"),
    max_budget: Optional[float] = Query(None, description="Maximum budget limit")
):
    results = gigs_db
    
    if category:
        results = [g for g in results if g["category"].lower() == category.lower()]
        
    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]
        
    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]
        
    return results


# 2. View details of a specific gig by its ID
@app.get("/gigs/{gig_id}")
def get_gig_by_id(gig_id: int):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig
    raise HTTPException(status_code=404, detail="Gig profile not found")


# 3. Search for gigs by title
@app.get("/gigs/search")
def search_gigs(q: str = Query(..., description="Query search string matches title")):
    results = [g for g in gigs_db if q.lower() in g["title"].lower()]
    return results


# 4. Create a new gig
@app.post("/gigs", status_code=201)
def create_gig(gig: GigCreate):
    # Auto-incrementing internal IDs
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1
    
    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",  # Fixed per registration number parameters
        "status": "Open",   # Initial status default setup
        "client_name": gig.client_name
    }
    
    gigs_db.append(new_gig)
    return {"message": "Gig published successfully", "gig": new_gig}


# 5. Update a gig's budget or status
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget
            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status
            return {"message": "Gig records updated successfully", "gig": gigs_db[index]}
            
    raise HTTPException(status_code=404, detail="Gig profile not found")


# 6. Delete a gig
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)
            return {"message": "Gig removed successfully from listing", "gig": deleted_gig}
            
    raise HTTPException(status_code=404, detail="Gig profile not found")