from typing import List, Any

from data_manager.orm import Result, ProcessingStep

from sqlalchemy.orm import Session
from sqlalchemy import select


def insert_collection_result(
    session: Session, kind: str, processing_step: ProcessingStep, data
) -> None:
    nRows = len(data)
    assert nRows > 0

    try:
        # Matrix
        nCols = len(data[0])
        assert nCols > 0

        try:
            len(data[0][0])
            raise RuntimeError("More than 2D objects (matrices) not yet supported")
        except:
            pass

        for row in range(nRows):
            for col in range(len(data[row])):
                current = Result(
                    kind=kind, processing_step=processing_step, data=data[row][col]
                )
                current.properties["kind"] = "Matrix"
                current.properties["indexing"] = "1-based"
                current.properties["row"] = str(row + 1)
                current.properties["column"] = str(col + 1)
                current.properties["original_collection_type"] = type(data).__name__
                current.properties["total_dimension"] = "{},{}".format(nRows, nCols)

    except TypeError:
        # Array
        for i in range(nRows):
            current = Result(kind=kind, processing_step=processing_step, data=data[i])
            current.properties["kind"] = "List"
            current.properties["indexing"] = "1-based"
            current.properties["index"] = str(i + 1)
            current.properties["original_collection_type"] = type(data).__name__
            current.properties["total_dimension"] = "{}".format(nRows)


def get_collection_result(
    session: Session, kind: str, processing_step: ProcessingStep
) -> List[Any]:
    result_set = session.scalars(
        select(Result)
        .where(Result.kind == kind)
        .where(Result.processing_step_id == processing_step.id)
    ).all()

    assert len(result_set) > 0

    data_kind: str = result_set[0].properties["kind"]

    data: List[Any] = []
    for current in result_set:
        if current.properties["kind"] != data_kind:
            raise RuntimeError(
                "The same dataset includes different kinds of data - this is not supported (and a bug?)"
            )
        assert current.properties["indexing"] == "1-based"
        if data_kind == "List":
            index = int(current.properties["index"]) - 1
            assert index >= 0

            if index + 1 > len(data):
                data.extend([None] * (index + 1 - len(data)))

            data[index] = current.data
        else:
            assert data_kind == "Matrix"
            row = int(current.properties["row"]) - 1
            col = int(current.properties["column"]) - 1
            assert row >= 0
            assert col >= 0

            for _ in range(row + 1 - len(data)):
                data.append([])

            if col + 1 > len(data[row]):
                data[row].extend([None] * (col + 1 - len(data[row])))

            data[row][col] = current.data

    return data
