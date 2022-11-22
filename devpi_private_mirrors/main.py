from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Tuple,
    Type,
)

from devpi_server.mirror import MirrorStage
from devpi_server.model import (
    BaseStage,
    BaseStageCustomizer,
    PrivateStage,
    SimplelinkMeta,
    SimpleLinks,
)
from pluggy import HookimplMarker

server_hookimpl = HookimplMarker("devpiserver")


class PrivateStageWithPrivateBaseSupport(BaseStageCustomizer):
    def get_versions_filter_iter(self, project: str, versions: list) -> Iterable[bool]:
        """Filter package versions."""
        is_private_found = False
        allowed_versions: set[str] = set()
        stage: PrivateStage = self.stage
        base_stage_names: tuple[str] = stage.ixconfig.get("bases", ())
        for base_stage_name in base_stage_names:
            base_stage: BaseStage = stage.model.getstage(base_stage_name)
            is_private: bool = base_stage.ixconfig.get("private_base", False)
            # skip unsupported stages
            if not isinstance(base_stage, (MirrorStage, PrivateStage)):
                continue
            # skip public ones
            if not is_private:
                continue
            if not base_stage.has_project_perstage(project):
                continue
            # project found, check links
            is_private_found = True
            base_versions: set[str] = base_stage.list_versions_perstage(project)
            for version in base_versions:
                allowed_versions.add(version)
        if not is_private_found:
            return None
        for version in versions:
            if version in allowed_versions:
                yield True
            else:
                yield False

    def get_simple_links_filter_iter(self, project: str, links: SimpleLinks) -> Iterable[bool]:
        """Filter package links."""
        input_links: list[SimplelinkMeta] = links._links
        allowed_links: set[str] = set()
        is_private_found = False
        stage: PrivateStage = self.stage
        base_stage_names: tuple[str] = stage.ixconfig.get("bases", ())
        for base_stage_name in base_stage_names:
            base_stage: BaseStage = stage.model.getstage(base_stage_name)
            is_private: bool = base_stage.ixconfig.get("private_base", False)
            # skip unsupported stages
            if not isinstance(base_stage, (MirrorStage, PrivateStage)):
                continue
            # skip public ones
            if not is_private:
                continue
            if not base_stage.has_project_perstage(project):
                continue
            # project found, check links
            is_private_found = True
            base_links = base_stage.get_simplelinks_perstage(project)
            for link in base_links:
                allowed_links.add(link.href)
        if not is_private_found:
            return None
        # expecting private and public repos has different links
        for link in input_links:
            if link.href in allowed_links:
                yield True
            else:
                yield False


@server_hookimpl  # type: ignore
def devpiserver_get_stage_customizer_classes() -> List[Tuple[str, Type[BaseStageCustomizer]]]:
    """Register new stage class."""
    return [("stage_private_base", PrivateStageWithPrivateBaseSupport)]


@server_hookimpl  # type: ignore
def devpiserver_indexconfig_defaults(index_type: str) -> Dict[str, Any]:
    """Add config option to all index types."""
    return {'private_base': False}
