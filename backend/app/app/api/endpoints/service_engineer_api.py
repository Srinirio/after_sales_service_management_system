from fastapi import *
from sqlalchemy.orm import *
from models import *
from typing import Annotated
from api.deps import *
from schemas import *
from crud import *
from datetime import *

router = APIRouter()

@router.get("/service_engineer/view/my_tickets",response_model=list[TicketsEngineerOut] | str)
async def viewTickets(
                     db: Annotated[Session, Depends(get_db)],
                     current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Here, service engineer can see the tickets assigned to him
    """
    db_data = db.query(
        Ticket.company_name,
        Ticket.address,
        Ticket.description,
        Ticket.company_name,
        Ticket.id,
        Ticket.created_at,
        TicketStatus.status_of_ticket
    ).join(
        AssigningTicket,
        AssigningTicket.ticket_id == Ticket.id
    ).outerjoin(
        TicketStatus,
        TicketStatus.ticket_id == Ticket.id 
    ).filter(
        AssigningTicket.assigned_to_emp_id == current_user.id
    ).order_by(AssigningTicket.id.desc(),AssigningTicket.created_at.desc()).all()
    
    if db_data:
        return db_data
    return "No Data"

@router.post("/service_engineer/{ticket_id}/update_ticket_status",response_model=Message)
async def createTicketStatus(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    ticket_id: Annotated[int, Path(...)],
    expected_date_to_complete: Annotated[datetime, Form(...)],
    priority: Annotated[int, Form(...,ge=1,le=3)]
):
    """
    here ,Service engineer can add expected date to complete and priority for the particular ticket
    
    - **Expected date to complete**: required
    - **Priority**: 1-> High , 2-> medium, 3-> low
    """
    checkTicketBelongsToHim(db=db,ticket_id=ticket_id,current_user=current_user)
    db_ticket = db.query(TicketStatus).filter(TicketStatus.ticket_id == ticket_id).one_or_none()
    
    if db_ticket:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Ticket status is already updated")
    
    ticket_status = TicketStatus(
        expected_date_to_complete = expected_date_to_complete,
        priority = priority,
        ticket_id = ticket_id
    )
    db.add(ticket_status)
    db.commit()
    return {"message":"Successfully Updated !!"}

@router.post("/service_engineer/add_expense/{ticket_id}",response_model=Message)
async def expense(
                 db: Annotated[Session, Depends(get_db)],
                 current_user: Annotated[User, Depends(get_current_user)],
                 ticket_id: Annotated[int, Path(...)],
                 description: Annotated[str, Form(...)],
                 amount: Annotated[float, Form(...)],
                 image: Annotated[UploadFile | None, File()] = None
):
    """
    Here, Service can add travel expense for the particular ticket
    """
    checkTicketBelongsToHim(db=db,ticket_id=ticket_id,current_user=current_user)
    return createExpense(db=db,ticket_id=ticket_id,
                               description=description,amount=amount,
                               emp_id=current_user,image=image)

@router.get("/service_engineer/all_materials",response_model=list[MaterialRequestResponse])
async def getMaterials(
                       db: Annotated[Session, Depends(get_db)],
                       current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Here, service engineer can see all the materials
    """
    db_material = db.query(Material.id,Material.material_name).all()
    if not db_material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No materials")
    return db_material


@router.post("/service_engineer/{ticket_id}/material_request/",response_model=Message)
async def materialRequest(
                         db: Annotated[Session, Depends(get_db)],
                         current_user: Annotated[User, Depends(get_current_user)],
                         ticket_id: Annotated[int, Path(...)],
                         material_id: Annotated[int, Body(...)],
                         units: Annotated[int, Body(...)]
):
    """
    Here, service engineer can make a material request to his ticket
    """
    checkTicketBelongsToHim(db=db,ticket_id=ticket_id,current_user=current_user)
    return createMaterialRequest(db=db,ticket_id=ticket_id,current_user=current_user,material_id=material_id,units=units)

@router.post("/service_engineer/add_work_report",response_model=Message)
async def workReport(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_user)],
                    data_in: WorkReportIn
):
    """
    - A Service Engineer can submit their work report for the current day.
    - If this is the employee's first work report, it will be accepted without issues.
    - If the employee is submitting their second work report, there is a validation to ensure that any pending work reports for previous days are submitted first.
    """
    if data_in.ticket_id is not None:
        checkTicketBelongsToHim(db=db,ticket_id=data_in.ticket_id,current_user=current_user)
        db_ticket_status = db.query(TicketStatus).filter(TicketStatus.ticket_id == data_in.ticket_id).one_or_none()
        if not db_ticket_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="Please update the ticket status and add your work report"
            )
    return createWorkReport(db=db,current_user=current_user,data_in=data_in)

@router.put("/service_engineer/{ticket_id}/completed",response_model=Message)
async def updateTicketStatusToCompleted(
                    db: Annotated[Session, Depends(get_db)],
                    current_user: Annotated[User, Depends(get_current_user)],
                    ticket_id: int
):
    """
    Here, service engineer can update the completed status of his ticket
    """
    checkTicketBelongsToHim(db=db,ticket_id=ticket_id,current_user=current_user)
    db_ticket_status = db.query(TicketStatus).filter(TicketStatus.ticket_id == ticket_id).one_or_none()
    if not db_ticket_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please update the expected date to complete and priority of ticket"
        )
    if db_ticket_status.status_of_ticket:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket status is already completed"
        )
    db_ticket_status.status_of_ticket = True
    db_ticket_status.completed_date = datetime.now()
    db.add(db_ticket_status)
    db.commit()
    return {"message":"Ticket status is completed !!"}
    
    
    



    
    
    
    
    
    

    
    
    
    
