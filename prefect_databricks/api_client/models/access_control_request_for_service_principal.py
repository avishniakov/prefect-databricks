from typing import Any, Dict, List, Type, TypeVar, Union

from pydantic import BaseModel, Field

from ..models.can_manage import CanManage
from ..models.can_manage_run import CanManageRun
from ..models.can_view import CanView
from ..models.is_owner import IsOwner
from ..types import UNSET, Unset

T = TypeVar("T", bound="AccessControlRequestForServicePrincipal")


class AccessControlRequestForServicePrincipal(BaseModel):
    """
    Attributes:
        permission_level (Union[CanManage, CanManageRun, CanView, IsOwner, Unset]): Permission level to grant.
        service_principal_name (Union[Unset, str]): Name of an Azure service principal. Example:
            9f0621ee-b52b-11ea-b3de-0242ac130004.
    """

    permission_level: Union[CanManage, CanManageRun, CanView, IsOwner, Unset] = UNSET
    service_principal_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        permission_level: Union[Unset, str]
        if isinstance(self.permission_level, Unset):
            permission_level = UNSET

        elif isinstance(self.permission_level, CanManage):
            permission_level = self.permission_level.value

        elif isinstance(self.permission_level, CanManageRun):
            permission_level = self.permission_level.value

        elif isinstance(self.permission_level, CanView):
            permission_level = self.permission_level.value

        else:
            permission_level = self.permission_level.value

        service_principal_name = self.service_principal_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if permission_level is not UNSET:
            field_dict["permission_level"] = permission_level
        if service_principal_name is not UNSET:
            field_dict["service_principal_name"] = service_principal_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        if src_dict is None or src_dict is UNSET:
            return {}
        d = {k: v if v is not None else UNSET for k, v in src_dict.items()}

        def _parse_permission_level(
            data: object,
        ) -> Union[CanManage, CanManageRun, CanView, IsOwner, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_permission_level_type_0 = CanManage(data)

                return componentsschemas_permission_level_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_permission_level_type_1 = CanManageRun(data)

                return componentsschemas_permission_level_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                componentsschemas_permission_level_type_2 = CanView(data)

                return componentsschemas_permission_level_type_2
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            componentsschemas_permission_level_type_3 = IsOwner(data)

            return componentsschemas_permission_level_type_3

        permission_level = _parse_permission_level(d.pop("permission_level", UNSET))

        service_principal_name = d.pop("service_principal_name", UNSET)

        access_control_request_for_service_principal = cls(
            permission_level=permission_level,
            service_principal_name=service_principal_name,
        )

        access_control_request_for_service_principal.additional_properties = d
        return access_control_request_for_service_principal

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
