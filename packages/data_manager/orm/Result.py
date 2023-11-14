from .Base import Base

from typing import Dict

from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    processing_step_id: Mapped[int] = mapped_column(
        ForeignKey("processing_steps.id", onupdate="CASCADE", ondelete="CASCADE")
    )
    kind: Mapped[str]
    _data_value: Mapped[str]
    _data_type: Mapped[str]
    _properties: Mapped[Dict[str, "ResultProperty"]] = relationship(
        collection_class=attribute_keyed_dict("keyword"), passive_deletes=True
    )

    properties: AssociationProxy[Dict[str, str]] = association_proxy(
        target_collection="_properties",
        attr="value",
        creator=lambda k, v: ResultProperty(keyword=k, value=v),
    )

    processing_step: Mapped["ProcessingStep"] = relationship(back_populates="results")  # type: ignore

    @property
    def data(self):
        if self._data_type == "int":
            return int(self._data_value)
        if self._data_type == "float":
            return float(self._data_value)
        elif self._data_type == "str":
            return str(self._data_value)

    @data.setter
    def data(self, value):
        if type(value) == int:
            self._data_type = "int"
        elif type(value) == float:
            self._data_type = "float"
        elif type(value) == str:
            self._data_type = "str"
        elif type(value) == list:
            raise RuntimeError(
                "Adding lists directly is not supported. Use insert_collection_result from the utils module instead"
            )
        else:
            raise RuntimeError("Unsupported data type: " + str(type(value)))

        self._data_value = str(value)


class ResultProperty(Base):
    __tablename__ = "result_properties"

    result_id: Mapped[int] = mapped_column(
        ForeignKey(Result.id, onupdate="CASCADE", ondelete="CASCADE"), primary_key=True
    )
    keyword: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]
