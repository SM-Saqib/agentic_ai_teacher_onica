"""Slide API Routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.database.models import Slide, SlideExplanation
from app.vector_store import chroma_store
from app.api.v1.schemas.slides import SlideCreate, SlideResponse, SlideExplanationCreate, SlideExplanationResponse

router = APIRouter(prefix="/api/v1/slides", tags=["slides"])


@router.post("/", response_model=SlideResponse)
async def create_slide(
    slide: SlideCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new slide"""
    # Create slide in database
    db_slide = Slide(
        title=slide.title,
        content=slide.content,
        description=slide.description,
        is_prebuilt=slide.is_prebuilt,
        version=slide.version,
    )

    db.add(db_slide)
    await db.commit()
    await db.refresh(db_slide)

    # Index in vector store
    try:
        embedding_id = await chroma_store.add_slide(
            slide_id=db_slide.id,
            title=db_slide.title,
            content=db_slide.content,
            metadata={
                "description": db_slide.description,
                "is_prebuilt": db_slide.is_prebuilt,
                "version": db_slide.version,
            }
        )
        # Update embedding_id in database
        db_slide.embedding_id = embedding_id
        await db.commit()
    except Exception as e:
        # Log error but don't fail the request
        print(f"Failed to index slide {db_slide.id}: {e}")

    return SlideResponse.from_orm(db_slide)


@router.get("/", response_model=List[SlideResponse])
async def list_slides(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all available slides"""
    result = await db.execute(
        select(Slide).offset(offset).limit(limit)
    )
    slides = result.scalars().all()
    return [SlideResponse.from_orm(slide) for slide in slides]


@router.get("/{slide_id}", response_model=SlideResponse)
async def get_slide(
    slide_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific slide"""
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id)
    )
    slide = result.scalars().first()

    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )

    return SlideResponse.from_orm(slide)


@router.put("/{slide_id}", response_model=SlideResponse)
async def update_slide(
    slide_id: int,
    slide_update: SlideCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a slide"""
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id)
    )
    slide = result.scalars().first()

    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )

    # Update fields
    for field, value in slide_update.dict().items():
        setattr(slide, field, value)

    slide.updated_at = None  # Trigger auto-update

    await db.commit()
    await db.refresh(slide)

    # Re-index in vector store
    try:
        if slide.embedding_id:
            await chroma_store.delete_slide(slide_id)

        embedding_id = await chroma_store.add_slide(
            slide_id=slide.id,
            title=slide.title,
            content=slide.content,
            metadata={
                "description": slide.description,
                "is_prebuilt": slide.is_prebuilt,
                "version": slide.version,
            }
        )
        slide.embedding_id = embedding_id
        await db.commit()
    except Exception as e:
        print(f"Failed to re-index slide {slide.id}: {e}")

    return SlideResponse.from_orm(slide)


@router.delete("/{slide_id}")
async def delete_slide(
    slide_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a slide"""
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id)
    )
    slide = result.scalars().first()

    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )

    # Delete from vector store
    try:
        await chroma_store.delete_slide(slide_id)
    except Exception as e:
        print(f"Failed to delete slide {slide_id} from vector store: {e}")

    # Delete from database
    await db.delete(slide)
    await db.commit()

    return {"message": "Slide deleted successfully"}


@router.post("/{slide_id}/explanations", response_model=SlideExplanationResponse)
async def create_slide_explanation(
    slide_id: int,
    explanation: SlideExplanationCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create an explanation for a slide"""
    # Verify slide exists
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id)
    )
    slide = result.scalars().first()

    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Slide not found"
        )

    # Create explanation in database
    db_explanation = SlideExplanation(
        slide_id=slide_id,
        explanation=explanation.explanation,
        language=explanation.language,
    )

    db.add(db_explanation)
    await db.commit()
    await db.refresh(db_explanation)

    # Index in vector store
    try:
        embedding_id = await chroma_store.add_slide_explanation(
            explanation_id=db_explanation.id,
            slide_id=slide_id,
            explanation=db_explanation.explanation,
            language=db_explanation.language,
        )
        # Update embedding_id in database
        db_explanation.embedding_id = embedding_id
        await db.commit()
    except Exception as e:
        print(f"Failed to index explanation {db_explanation.id}: {e}")

    return SlideExplanationResponse.from_orm(db_explanation)


@router.get("/{slide_id}/explanations", response_model=List[SlideExplanationResponse])
async def list_slide_explanations(
    slide_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List explanations for a slide"""
    result = await db.execute(
        select(SlideExplanation).where(SlideExplanation.slide_id == slide_id)
    )
    explanations = result.scalars().all()
    return [SlideExplanationResponse.from_orm(exp) for exp in explanations]


@router.post("/search")
async def search_slides(
    query: str,
    limit: int = 5,
    slide_id: Optional[int] = None,
    current_user: dict = Depends(get_current_user),
):
    """Search for similar slides using vector similarity"""
    try:
        results = await chroma_store.search_similar(
            query=query,
            n_results=limit,
            where={"type": "slide"} if slide_id is None else {"type": "slide", "slide_id": str(slide_id)}
        )

        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
