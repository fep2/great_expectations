from unittest import mock

import pytest
from ruamel.yaml import YAML

import great_expectations.exceptions as ge_exceptions
from great_expectations import DataContext
from great_expectations.core import IDDict
from great_expectations.core.batch import (
    BatchDefinition,
    BatchRequest,
    BatchRequestBase,
)
from great_expectations.data_context.util import instantiate_class_from_config
from great_expectations.datasource.data_connector import ConfiguredAssetGCSDataConnector

yaml = YAML()


@pytest.fixture
def expected_config_dict():
    """Used to validate `self_check()` and `test_yaml_config()` outputs."""
    config = {
        "class_name": "ConfiguredAssetGCSDataConnector",
        "data_asset_count": 1,
        "example_data_asset_names": [
            "alpha",
        ],
        "data_assets": {
            "alpha": {
                "example_data_references": [
                    "alpha-1.csv",
                    "alpha-2.csv",
                    "alpha-3.csv",
                ],
                "batch_definition_count": 3,
            },
        },
        "example_unmatched_data_references": [],
        "unmatched_data_reference_count": 0,
    }
    return config


@pytest.fixture
def expected_batch_definitions_unsorted():
    """
    Used to validate `get_batch_definition_list_from_batch_request()` outputs.
    Input and output should maintain the same order (henced "unsorted")
    """
    expected = [
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "alex", "timestamp": "20200809", "price": "1000"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "eugene", "timestamp": "20200809", "price": "1500"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200811", "price": "1009"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "abe", "timestamp": "20200809", "price": "1040"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "will", "timestamp": "20200809", "price": "1002"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200713", "price": "1567"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "eugene", "timestamp": "20201129", "price": "1900"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "will", "timestamp": "20200810", "price": "1001"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200810", "price": "1003"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "alex", "timestamp": "20200819", "price": "1300"}
            ),
        ),
    ]
    return expected


@pytest.fixture
def expected_batch_definitions_sorted():
    """
    Used to validate `get_batch_definition_list_from_batch_request()` outputs.
    Input should be sorted based on some criteria, resulting in some change
    between input and output.
    """
    expected = [
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "abe", "timestamp": "20200809", "price": "1040"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "alex", "timestamp": "20200819", "price": "1300"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "alex", "timestamp": "20200809", "price": "1000"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "eugene", "timestamp": "20201129", "price": "1900"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "eugene", "timestamp": "20200809", "price": "1500"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200811", "price": "1009"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200810", "price": "1003"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "james", "timestamp": "20200713", "price": "1567"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "will", "timestamp": "20200810", "price": "1001"}
            ),
        ),
        BatchDefinition(
            datasource_name="test_environment",
            data_connector_name="general_gcs_data_connector",
            data_asset_name="TestFiles",
            batch_identifiers=IDDict(
                {"name": "will", "timestamp": "20200809", "price": "1002"}
            ),
        ),
    ]
    return expected


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_instantiation_without_args(
    mock_gcs_conn, mock_list_keys, expected_config_dict
):
    my_data_connector = ConfiguredAssetGCSDataConnector(
        name="my_data_connector",
        datasource_name="FAKE_DATASOURCE_NAME",
        default_regex={
            "pattern": "alpha-(.*)\\.csv",
            "group_names": ["index"],
        },
        bucket_or_name="my_bucket",
        prefix="",
        assets={"alpha": {}},
    )
    assert my_data_connector.self_check() == expected_config_dict

    my_data_connector._refresh_data_references_cache()
    assert my_data_connector.get_data_reference_list_count() == 3
    assert my_data_connector.get_unmatched_data_references() == []


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.service_account.Credentials.from_service_account_file"
)
def test_instantiation_with_filename_arg(
    mock_auth_method, mock_gcs_conn, mock_list_keys, expected_config_dict
):
    my_data_connector = ConfiguredAssetGCSDataConnector(
        name="my_data_connector",
        datasource_name="FAKE_DATASOURCE_NAME",
        gcs_options={
            "filename": "my_filename.json",
        },
        default_regex={
            "pattern": "alpha-(.*)\\.csv",
            "group_names": ["index"],
        },
        bucket_or_name="my_bucket",
        prefix="",
        assets={"alpha": {}},
    )

    assert my_data_connector.self_check() == expected_config_dict

    my_data_connector._refresh_data_references_cache()
    assert my_data_connector.get_data_reference_list_count() == 3
    assert my_data_connector.get_unmatched_data_references() == []


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.service_account.Credentials.from_service_account_info"
)
def test_instantiation_with_info_arg(
    mock_auth_method, mock_gcs_conn, mock_list_keys, expected_config_dict
):
    my_data_connector = ConfiguredAssetGCSDataConnector(
        name="my_data_connector",
        datasource_name="FAKE_DATASOURCE_NAME",
        gcs_options={
            "info": "{ my_json: my_content }",
        },
        default_regex={
            "pattern": "alpha-(.*)\\.csv",
            "group_names": ["index"],
        },
        bucket_or_name="my_bucket",
        prefix="",
        assets={"alpha": {}},
    )

    assert my_data_connector.self_check() == expected_config_dict

    my_data_connector._refresh_data_references_cache()
    assert my_data_connector.get_data_reference_list_count() == 3
    assert my_data_connector.get_unmatched_data_references() == []


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_instantiation_with_test_yaml_config(
    mock_gcs_conn,
    mock_list_keys,
    mock_emit,
    empty_data_context_stats_enabled,
    expected_config_dict,
):
    context: DataContext = empty_data_context_stats_enabled

    report_object = context.test_yaml_config(
        f"""
        module_name: great_expectations.datasource.data_connector
        class_name: ConfiguredAssetGCSDataConnector
        datasource_name: FAKE_DATASOURCE
        name: TEST_DATA_CONNECTOR
        default_regex:
            pattern: alpha-(.*)\\.csv
            group_names:
                - index
        bucket_or_name: my_bucket
        prefix: ""
        assets:
            alpha:
    """,
        return_mode="report_object",
    )

    assert report_object == expected_config_dict


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_instantiation_with_test_yaml_config_emits_proper_payload(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    context: DataContext = empty_data_context_stats_enabled

    context.test_yaml_config(
        f"""
        module_name: great_expectations.datasource.data_connector
        class_name: ConfiguredAssetGCSDataConnector
        datasource_name: FAKE_DATASOURCE
        name: TEST_DATA_CONNECTOR
        default_regex:
            pattern: alpha-(.*)\\.csv
            group_names:
                - index
        bucket_or_name: my_bucket
        prefix: ""
        assets:
            alpha:
    """,
        return_mode="report_object",
    )
    assert mock_emit.call_count == 1

    anonymized_name = mock_emit.call_args_list[0][0][0]["event_payload"][
        "anonymized_name"
    ]
    expected_call_args_list = [
        mock.call(
            {
                "event": "data_context.test_yaml_config",
                "event_payload": {
                    "anonymized_name": anonymized_name,
                    "parent_class": "ConfiguredAssetGCSDataConnector",
                },
                "success": True,
            }
        ),
    ]
    assert mock_emit.call_args_list == expected_call_args_list


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_instantiation_from_a_config_with_nonmatching_regex_creates_unmatched_references(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    context: DataContext = empty_data_context_stats_enabled

    report_object = context.test_yaml_config(
        f"""
        module_name: great_expectations.datasource.data_connector
        class_name: ConfiguredAssetGCSDataConnector
        datasource_name: FAKE_DATASOURCE
        name: TEST_DATA_CONNECTOR
        default_regex:
            pattern: beta-(.*)\\.csv
            group_names:
                - index
        bucket_or_name: my_bucket
        prefix: ""
        assets:
            alpha:
    """,
        return_mode="report_object",
    )

    assert report_object == {
        "class_name": "ConfiguredAssetGCSDataConnector",
        "data_asset_count": 1,
        "example_data_asset_names": [
            "alpha",
        ],
        "data_assets": {
            "alpha": {"example_data_references": [], "batch_definition_count": 0},
        },
        "example_unmatched_data_references": [
            "alpha-1.csv",
            "alpha-2.csv",
            "alpha-3.csv",
        ],
        "unmatched_data_reference_count": 3,
    }


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
    return_value=["alpha-1.csv", "alpha-2.csv", "alpha-3.csv"],
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_get_batch_definition_list_from_batch_request_with_nonexistent_datasource_name_raises_error(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector = ConfiguredAssetGCSDataConnector(
        name="my_data_connector",
        datasource_name="FAKE_DATASOURCE_NAME",
        default_regex={
            "pattern": "alpha-(.*)\\.csv",
            "group_names": ["index"],
        },
        bucket_or_name="my_bucket",
        prefix="",
        assets={"alpha": {}},
    )

    # Raises error in `DataConnector._validate_batch_request()` due to `datasource_name` in BatchRequest not matching DataConnector `datasource_name`
    with pytest.raises(ValueError):
        my_data_connector.get_batch_definition_list_from_batch_request(
            BatchRequest(
                datasource_name="something",
                data_connector_name="my_data_connector",
                data_asset_name="something",
            )
        )


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_get_definition_list_from_batch_request_with_empty_args_raises_error(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector_yaml = yaml.load(
        f"""
           class_name: ConfiguredAssetGCSDataConnector
           datasource_name: test_environment
           execution_engine:
               class_name: PandasExecutionEngine
           bucket_or_name: my_bucket
           prefix: ""
           assets:
               TestFiles:
           default_regex:
               pattern: (.+)_(.+)_(.+)\\.csv
               group_names:
                   - name
                   - timestamp
                   - price
       """,
    )

    mock_list_keys.return_value = (
        [
            "alex_20200809_1000.csv",
            "eugene_20200809_1500.csv",
            "james_20200811_1009.csv",
            "abe_20200809_1040.csv",
            "will_20200809_1002.csv",
            "james_20200713_1567.csv",
            "eugene_20201129_1900.csv",
            "will_20200810_1001.csv",
            "james_20200810_1003.csv",
            "alex_20200819_1300.csv",
        ],
    )

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    # Raises error in `FilePathDataConnector.get_batch_definition_list_from_batch_request()` due to missing a `batch_request` arg
    with pytest.raises(TypeError):
        my_data_connector.get_batch_definition_list_from_batch_request()


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_get_definition_list_from_batch_request_with_unnamed_data_asset_name_raises_error(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector_yaml = yaml.load(
        f"""
           class_name: ConfiguredAssetGCSDataConnector
           datasource_name: test_environment
           execution_engine:
               class_name: PandasExecutionEngine
           bucket_or_name: my_bucket
           prefix: ""
           assets:
               TestFiles:
           default_regex:
               pattern: (.+)_(.+)_(.+)\\.csv
               group_names:
                   - name
                   - timestamp
                   - price
       """,
    )

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    # Raises error in `Batch._validate_init_parameters()` due to `data_asset_name` being `NoneType` and not the required `str`
    with pytest.raises(TypeError):
        my_data_connector.get_batch_definition_list_from_batch_request(
            BatchRequest(
                datasource_name="test_environment",
                data_connector_name="general_gcs_data_connector",
                data_asset_name=None,
            )
        )


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_return_all_batch_definitions_unsorted_without_named_data_asset_name(
    mock_gcs_conn,
    mock_list_keys,
    mock_emit,
    empty_data_context_stats_enabled,
    expected_batch_definitions_unsorted,
):
    my_data_connector_yaml = yaml.load(
        f"""
           class_name: ConfiguredAssetGCSDataConnector
           datasource_name: test_environment
           execution_engine:
               class_name: PandasExecutionEngine
           bucket_or_name: my_bucket
           prefix: ""
           assets:
               TestFiles:
           default_regex:
               pattern: (.+)_(.+)_(.+)\\.csv
               group_names:
                   - name
                   - timestamp
                   - price
       """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    # In an actual production environment, GCS will automatically sort these blobs by path (alphabetic order).
    # Source: https://cloud.google.com/storage/docs/listing-objects
    #
    # The expected behavior is that our `unsorted_batch_definition_list` will maintain the same order it parses through `list_gcs_keys()` (hence "unsorted").
    # When using an actual `Client` (and not a mock), the output of `list_gcs_keys` would be pre-sorted by nature of how the system orders blobs.
    # It is important to note that although this is a minor deviation, it is deemed to be immaterial as we still end up testing our desired behavior.

    unsorted_batch_definition_list = (
        my_data_connector._get_batch_definition_list_from_batch_request(
            BatchRequestBase(
                datasource_name="test_environment",
                data_connector_name="general_gcs_data_connector",
                data_asset_name=None,
            )
        )
    )
    assert unsorted_batch_definition_list == expected_batch_definitions_unsorted


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_return_all_batch_definitions_unsorted_with_named_data_asset_name(
    mock_gcs_conn,
    mock_list_keys,
    mock_emit,
    empty_data_context_stats_enabled,
    expected_batch_definitions_unsorted,
):
    my_data_connector_yaml = yaml.load(
        f"""
           class_name: ConfiguredAssetGCSDataConnector
           datasource_name: test_environment
           execution_engine:
               class_name: PandasExecutionEngine
           bucket_or_name: my_bucket
           prefix: ""
           assets:
               TestFiles:
           default_regex:
               pattern: (.+)_(.+)_(.+)\\.csv
               group_names:
                   - name
                   - timestamp
                   - price
       """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    # In an actual production environment, GCS will automatically sort these blobs by path (alphabetic order).
    # Source: https://cloud.google.com/storage/docs/listing-objects
    #
    # The expected behavior is that our `unsorted_batch_definition_list` will maintain the same order it parses through `list_gcs_keys()` (hence "unsorted").
    # When using an actual `Client` (and not a mock), the output of `list_gcs_keys` would be pre-sorted by nature of how the system orders blobs.
    # It is important to note that although this is a minor deviation, it is deemed to be immaterial as we still end up testing our desired behavior.

    unsorted_batch_definition_list = (
        my_data_connector.get_batch_definition_list_from_batch_request(
            BatchRequest(
                datasource_name="test_environment",
                data_connector_name="general_gcs_data_connector",
                data_asset_name="TestFiles",
            )
        )
    )
    assert unsorted_batch_definition_list == expected_batch_definitions_unsorted


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_return_all_batch_definitions_basic_sorted(
    mock_gcs_conn,
    mock_list_keys,
    mock_emit,
    empty_data_context_stats_enabled,
    expected_batch_definitions_sorted,
):
    my_data_connector_yaml = yaml.load(
        f"""
       class_name: ConfiguredAssetGCSDataConnector
       datasource_name: test_environment
       execution_engine:
           class_name: PandasExecutionEngine
       bucket_or_name: my_bucket
       prefix: ""
       assets:
           TestFiles:
       default_regex:
           pattern: (.+)_(.+)_(.+)\\.csv
           group_names:
               - name
               - timestamp
               - price
       sorters:
           - orderby: asc
             class_name: LexicographicSorter
             name: name
           - datetime_format: "%Y%m%d"
             orderby: desc
             class_name: DateTimeSorter
             name: timestamp
           - orderby: desc
             class_name: NumericSorter
             name: price
     """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    self_check_report = my_data_connector.self_check()

    assert self_check_report["class_name"] == "ConfiguredAssetGCSDataConnector"
    assert self_check_report["data_asset_count"] == 1
    assert self_check_report["data_assets"]["TestFiles"]["batch_definition_count"] == 10
    assert self_check_report["unmatched_data_reference_count"] == 0

    sorted_batch_definition_list = (
        my_data_connector.get_batch_definition_list_from_batch_request(
            BatchRequest(
                datasource_name="test_environment",
                data_connector_name="general_gcs_data_connector",
                data_asset_name="TestFiles",
            )
        )
    )
    assert sorted_batch_definition_list == expected_batch_definitions_sorted


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
def test_return_all_batch_definitions_returns_specified_partition(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector_yaml = yaml.load(
        f"""
       class_name: ConfiguredAssetGCSDataConnector
       datasource_name: test_environment
       execution_engine:
           class_name: PandasExecutionEngine
       bucket_or_name: my_bucket
       prefix: ""
       assets:
           TestFiles:
       default_regex:
           pattern: (.+)_(.+)_(.+)\\.csv
           group_names:
               - name
               - timestamp
               - price
       sorters:
           - orderby: asc
             class_name: LexicographicSorter
             name: name
           - datetime_format: "%Y%m%d"
             orderby: desc
             class_name: DateTimeSorter
             name: timestamp
           - orderby: desc
             class_name: NumericSorter
             name: price
     """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    self_check_report = my_data_connector.self_check()

    assert self_check_report["class_name"] == "ConfiguredAssetGCSDataConnector"
    assert self_check_report["data_asset_count"] == 1
    assert self_check_report["data_assets"]["TestFiles"]["batch_definition_count"] == 10
    assert self_check_report["unmatched_data_reference_count"] == 0

    my_batch_request: BatchRequest = BatchRequest(
        datasource_name="test_environment",
        data_connector_name="general_gcs_data_connector",
        data_asset_name="TestFiles",
        data_connector_query=IDDict(
            **{
                "batch_filter_parameters": {
                    "name": "james",
                    "timestamp": "20200713",
                    "price": "1567",
                }
            }
        ),
    )

    my_batch_definition_list = (
        my_data_connector.get_batch_definition_list_from_batch_request(
            batch_request=my_batch_request
        )
    )

    assert len(my_batch_definition_list) == 1
    my_batch_definition = my_batch_definition_list[0]
    expected_batch_definition: BatchDefinition = BatchDefinition(
        datasource_name="test_environment",
        data_connector_name="general_gcs_data_connector",
        data_asset_name="TestFiles",
        batch_identifiers=IDDict(
            **{
                "name": "james",
                "timestamp": "20200713",
                "price": "1567",
            }
        ),
    )
    assert my_batch_definition == expected_batch_definition


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_return_all_batch_definitions_sorted_without_data_connector_query(
    mock_gcs_conn,
    mock_list_keys,
    mock_emit,
    empty_data_context_stats_enabled,
    expected_batch_definitions_sorted,
):
    my_data_connector_yaml = yaml.load(
        f"""
       class_name: ConfiguredAssetGCSDataConnector
       datasource_name: test_environment
       execution_engine:
           class_name: PandasExecutionEngine
       bucket_or_name: my_bucket
       prefix: ""
       assets:
           TestFiles:
       default_regex:
           pattern: (.+)_(.+)_(.+)\\.csv
           group_names:
               - name
               - timestamp
               - price
       sorters:
           - orderby: asc
             class_name: LexicographicSorter
             name: name
           - datetime_format: "%Y%m%d"
             orderby: desc
             class_name: DateTimeSorter
             name: timestamp
           - orderby: desc
             class_name: NumericSorter
             name: price
     """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config=my_data_connector_yaml,
        runtime_environment={
            "name": "general_gcs_data_connector",
            "datasource_name": "test_environment",
        },
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
    )

    self_check_report = my_data_connector.self_check()

    assert self_check_report["class_name"] == "ConfiguredAssetGCSDataConnector"
    assert self_check_report["data_asset_count"] == 1
    assert self_check_report["data_assets"]["TestFiles"]["batch_definition_count"] == 10
    assert self_check_report["unmatched_data_reference_count"] == 0

    sorted_batch_definition_list = (
        my_data_connector.get_batch_definition_list_from_batch_request(
            BatchRequest(
                datasource_name="test_environment",
                data_connector_name="general_gcs_data_connector",
                data_asset_name="TestFiles",
            )
        )
    )
    assert sorted_batch_definition_list == expected_batch_definitions_sorted


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_return_all_batch_definitions_raises_error_due_to_sorter_that_does_not_match_group(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector_yaml = yaml.load(
        f"""
       class_name: ConfiguredAssetGCSDataConnector
       datasource_name: test_environment
       execution_engine:
           class_name: PandasExecutionEngine
       bucket_or_name: my_bucket
       assets:
           TestFiles:
               pattern: (.+)_(.+)_(.+)\\.csv
               group_names:
                   - name
                   - timestamp
                   - price
       default_regex:
           pattern: (.+)_.+_.+\\.csv
           group_names:
               - name
       sorters:
           - orderby: asc
             class_name: LexicographicSorter
             name: name
           - datetime_format: "%Y%m%d"
             orderby: desc
             class_name: DateTimeSorter
             name: timestamp
           - orderby: desc
             class_name: NumericSorter
             name: for_me_Me_Me
   """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    # Raises error due to a sorter (for_me_Me_me) not matching a group_name in `FilePathDataConnector._validate_sorters_configuration()`
    with pytest.raises(ge_exceptions.DataConnectorError):
        instantiate_class_from_config(
            config=my_data_connector_yaml,
            runtime_environment={
                "name": "general_gcs_data_connector",
                "datasource_name": "test_environment",
            },
            config_defaults={
                "module_name": "great_expectations.datasource.data_connector"
            },
        )


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys"
)
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_return_all_batch_definitions_too_many_sorters(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    my_data_connector_yaml = yaml.load(
        f"""
       class_name: ConfiguredAssetGCSDataConnector
       datasource_name: test_environment
       execution_engine:
           class_name: PandasExecutionEngine
       bucket_or_name: my_bucket
       prefix: ""
       assets:
           TestFiles:
       default_regex:
           pattern: (.+)_.+_.+\\.csv
           group_names:
               - name
       sorters:
           - orderby: asc
             class_name: LexicographicSorter
             name: name
           - datetime_format: "%Y%m%d"
             orderby: desc
             class_name: DateTimeSorter
             name: timestamp
           - orderby: desc
             class_name: NumericSorter
             name: price
   """,
    )

    mock_list_keys.return_value = [
        "alex_20200809_1000.csv",
        "eugene_20200809_1500.csv",
        "james_20200811_1009.csv",
        "abe_20200809_1040.csv",
        "will_20200809_1002.csv",
        "james_20200713_1567.csv",
        "eugene_20201129_1900.csv",
        "will_20200810_1001.csv",
        "james_20200810_1003.csv",
        "alex_20200819_1300.csv",
    ]

    # Raises error due to a non-existent sorter being specified in `FilePathDataConnector._validate_sorters_configuration()`
    with pytest.raises(ge_exceptions.DataConnectorError):
        instantiate_class_from_config(
            config=my_data_connector_yaml,
            runtime_environment={
                "name": "general_gcs_data_connector",
                "datasource_name": "test_environment",
            },
            config_defaults={
                "module_name": "great_expectations.datasource.data_connector"
            },
        )


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
)
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_example_with_explicit_data_asset_names(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    yaml_string = f"""
class_name: ConfiguredAssetGCSDataConnector
datasource_name: FAKE_DATASOURCE_NAME
bucket_or_name: my_bucket
prefix: my_base_directory/
default_regex:
   pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.(csv|txt)$
   group_names:
       - data_asset_name
       - year_dir
       - month_dir
assets:
   alpha:
       prefix: my_base_directory/alpha/files/go/here/
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.csv$
   beta:
       prefix: my_base_directory/beta_here/
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.txt$
   gamma:
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.csv$
   """
    config = yaml.load(yaml_string)

    mock_list_keys.return_value = [  # Initial return value during instantiation
        "my_base_directory/alpha/files/go/here/alpha-202001.csv",
        "my_base_directory/alpha/files/go/here/alpha-202002.csv",
        "my_base_directory/alpha/files/go/here/alpha-202003.csv",
        "my_base_directory/beta_here/beta-202001.txt",
        "my_base_directory/beta_here/beta-202002.txt",
        "my_base_directory/beta_here/beta-202003.txt",
        "my_base_directory/beta_here/beta-202004.txt",
        "my_base_directory/gamma-202001.csv",
        "my_base_directory/gamma-202002.csv",
        "my_base_directory/gamma-202003.csv",
        "my_base_directory/gamma-202004.csv",
        "my_base_directory/gamma-202005.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config,
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
        runtime_environment={"name": "my_data_connector"},
    )

    # Since we are using mocks, we need to redefine the output of subsequent calls to `list_gcs_keys()`
    # Our patched object provides the ability to define a "side_effect", an iterable containing return
    # values for subsequent calls. Since `_refresh_data_references_cache()` makes multiple calls to
    # this method (once per asset), we define our expected behavior below.
    #
    # Source: https://stackoverflow.com/questions/24897145/python-mock-multiple-return-values

    mock_list_keys.side_effect = [
        [  # Asset alpha
            "my_base_directory/alpha/files/go/here/alpha-202001.csv",
            "my_base_directory/alpha/files/go/here/alpha-202002.csv",
            "my_base_directory/alpha/files/go/here/alpha-202003.csv",
        ],
        [  # Asset beta
            "my_base_directory/beta_here/beta-202001.txt",
            "my_base_directory/beta_here/beta-202002.txt",
            "my_base_directory/beta_here/beta-202003.txt",
            "my_base_directory/beta_here/beta-202004.txt",
        ],
        [  # Asset gamma
            "my_base_directory/gamma-202001.csv",
            "my_base_directory/gamma-202002.csv",
            "my_base_directory/gamma-202003.csv",
            "my_base_directory/gamma-202004.csv",
            "my_base_directory/gamma-202005.csv",
        ],
    ]

    my_data_connector._refresh_data_references_cache()

    assert len(my_data_connector.get_unmatched_data_references()) == 0

    assert (
        len(
            my_data_connector.get_batch_definition_list_from_batch_request(
                batch_request=BatchRequest(
                    datasource_name="FAKE_DATASOURCE_NAME",
                    data_connector_name="my_data_connector",
                    data_asset_name="alpha",
                )
            )
        )
        == 3
    )

    assert (
        len(
            my_data_connector.get_batch_definition_list_from_batch_request(
                batch_request=BatchRequest(
                    datasource_name="FAKE_DATASOURCE_NAME",
                    data_connector_name="my_data_connector",
                    data_asset_name="beta",
                )
            )
        )
        == 4
    )

    assert (
        len(
            my_data_connector.get_batch_definition_list_from_batch_request(
                batch_request=BatchRequest(
                    datasource_name="FAKE_DATASOURCE_NAME",
                    data_connector_name="my_data_connector",
                    data_asset_name="gamma",
                )
            )
        )
        == 5
    )


@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.storage.Client"
)
@mock.patch(
    "great_expectations.datasource.data_connector.configured_asset_gcs_data_connector.list_gcs_keys",
)
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_get_full_file_path(
    mock_gcs_conn, mock_list_keys, mock_emit, empty_data_context_stats_enabled
):
    yaml_string = f"""
class_name: ConfiguredAssetGCSDataConnector
datasource_name: FAKE_DATASOURCE_NAME
bucket_or_name: my_bucket
prefix: my_base_directory/
default_regex:
   pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.(csv|txt)$
   group_names:
       - data_asset_name
       - year_dir
       - month_dir
assets:
   alpha:
       prefix: my_base_directory/alpha/files/go/here/
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.csv$
   beta:
       prefix: my_base_directory/beta_here/
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.txt$
   gamma:
       pattern: ^(.+)-(\\d{{4}})(\\d{{2}})\\.csv$
   """
    config = yaml.load(yaml_string)

    mock_list_keys.return_value = [
        "my_base_directory/alpha/files/go/here/alpha-202001.csv",
        "my_base_directory/alpha/files/go/here/alpha-202002.csv",
        "my_base_directory/alpha/files/go/here/alpha-202003.csv",
        "my_base_directory/beta_here/beta-202001.txt",
        "my_base_directory/beta_here/beta-202002.txt",
        "my_base_directory/beta_here/beta-202003.txt",
        "my_base_directory/beta_here/beta-202004.txt",
        "my_base_directory/gamma-202001.csv",
        "my_base_directory/gamma-202002.csv",
        "my_base_directory/gamma-202003.csv",
        "my_base_directory/gamma-202004.csv",
        "my_base_directory/gamma-202005.csv",
    ]

    my_data_connector: ConfiguredAssetGCSDataConnector = instantiate_class_from_config(
        config,
        config_defaults={"module_name": "great_expectations.datasource.data_connector"},
        runtime_environment={"name": "my_data_connector"},
    )

    assert (
        my_data_connector._get_full_file_path(
            "my_base_directory/alpha/files/go/here/alpha-202001.csv", "alpha"
        )
        == "gs://my_bucket/my_base_directory/alpha/files/go/here/alpha-202001.csv"
    )
    assert (
        my_data_connector._get_full_file_path(
            "my_base_directory/beta_here/beta-202002.txt", "beta"
        )
        == "gs://my_bucket/my_base_directory/beta_here/beta-202002.txt"
    )
    assert (
        my_data_connector._get_full_file_path(
            "my_base_directory/gamma-202005.csv", "gamma"
        )
        == "gs://my_bucket/my_base_directory/gamma-202005.csv"
    )
